"""Agent base classes + LLM provider abstraction.

Provider chain (selected by `LLM.from_env()`):

    ANTHROPIC_API_KEY  -> Anthropic Claude
    OPENAI_API_KEY     -> OpenAI gpt-4o-mini
    GROQ_API_KEY       -> Groq llama-3.3-70b-versatile
    ASI1_API_KEY       -> Fetch.ai ASI1-Mini
    (none)             -> StubProvider

Whichever provider is primary, ASI1-Mini (when available) is wired as
fallback so a transient outage does not break the tutor stream. Each call
applies a bounded retry with exponential backoff and a per-attempt timeout.
"""

from __future__ import annotations

import abc
import asyncio
import logging
import os
import random
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Protocol

import httpx

log = logging.getLogger("sage.agents")


# ----- Trace / context ----------------------------------------------------


@dataclass
class AgentMessage:
    sender: str
    recipient: str
    intent: str  # "request" | "response" | "broadcast"
    payload: dict[str, Any] = field(default_factory=dict)
    trace_id: str = ""


@dataclass
class AgentContext:
    """Shared state passed through the swarm for one tutoring turn."""

    session_id: int
    user_id: int
    user_message: str
    a11y: dict[str, Any] = field(default_factory=dict)
    mastery: list[dict[str, Any]] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    retrieved: list[dict[str, Any]] = field(default_factory=list)
    plan: dict[str, Any] = field(default_factory=dict)
    answer: str = ""
    verification: dict[str, Any] = field(default_factory=dict)
    concept_map_delta: list[dict[str, Any]] = field(default_factory=list)
    assessment: dict[str, Any] = field(default_factory=dict)
    peers: list[dict[str, Any]] = field(default_factory=list)
    progress_delta: dict[str, Any] = field(default_factory=dict)
    trace: list[AgentMessage] = field(default_factory=list)


# ----- Retry helper -------------------------------------------------------


_NON_RETRYABLE_STATUSES = frozenset({400, 401, 403, 404, 422})


async def with_retry(
    fn: Callable[[], Awaitable[str]],
    *,
    attempts: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 4.0,
) -> str:
    """Call `fn` up to `attempts` times with jittered exponential backoff.

    4xx client errors (auth, validation, not-found) are NOT retried — those
    are deterministic and re-issuing the same request just wastes time and
    burns rate-limit budget on the upstream provider.
    """
    last: Exception | None = None
    for i in range(attempts):
        try:
            return await fn()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in _NON_RETRYABLE_STATUSES:
                raise
            last = exc
        except httpx.HTTPError as exc:
            last = exc
        except Exception:
            # Non-retryable
            raise

        if i == attempts - 1:
            break
        sleep = min(base_delay * (2**i), max_delay) + random.uniform(0, 0.25)
        log.warning("LLM attempt %d failed: %s — retrying in %.2fs", i + 1, last, sleep)
        await asyncio.sleep(sleep)

    assert last is not None
    raise last


# ----- Providers ----------------------------------------------------------


class LLMProvider(Protocol):
    name: str

    async def complete(self, system: str, user: str, **kw: Any) -> str: ...


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, api_key: str, model: str = "claude-opus-4-7", timeout: float = 30.0):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    async def complete(self, system: str, user: str, **kw: Any) -> str:
        async def _call() -> str:
            async with httpx.AsyncClient(timeout=self.timeout) as c:
                r = await c.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "max_tokens": kw.get("max_tokens", 1024),
                        "system": system,
                        "messages": [{"role": "user", "content": user}],
                    },
                )
                r.raise_for_status()
                data = r.json()
                return "".join(b.get("text", "") for b in data.get("content", []))

        return await with_retry(_call)


class _OpenAICompatProvider:
    """Shared base for OpenAI-protocol providers (OpenAI, Groq, ASI1)."""

    name = "openai-compat"
    base_url = ""

    def __init__(self, api_key: str, model: str, timeout: float = 30.0):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    async def complete(self, system: str, user: str, **kw: Any) -> str:
        async def _call() -> str:
            async with httpx.AsyncClient(timeout=self.timeout) as c:
                r = await c.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "content-type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "max_tokens": kw.get("max_tokens", 1024),
                        "messages": [
                            {"role": "system", "content": system},
                            {"role": "user", "content": user},
                        ],
                    },
                )
                r.raise_for_status()
                data = r.json()
                return data["choices"][0]["message"]["content"]

        return await with_retry(_call)


class OpenAIProvider(_OpenAICompatProvider):
    name = "openai"
    base_url = "https://api.openai.com/v1"

    def __init__(self, api_key: str, model: str = "gpt-4o-mini", timeout: float = 30.0):
        super().__init__(api_key, model, timeout)


class GroqProvider(_OpenAICompatProvider):
    name = "groq"
    base_url = "https://api.groq.com/openai/v1"

    def __init__(
        self, api_key: str, model: str = "llama-3.3-70b-versatile", timeout: float = 30.0
    ):
        super().__init__(api_key, model, timeout)


class ASI1MiniProvider(_OpenAICompatProvider):
    name = "asi1-mini"
    base_url = "https://api.asi1.ai/v1"

    def __init__(self, api_key: str, model: str = "asi1-mini", timeout: float = 30.0):
        super().__init__(api_key, model, timeout)


class StubProvider:
    """Offline default — used when no API keys are configured."""

    name = "stub"

    async def complete(self, system: str, user: str, **kw: Any) -> str:  # noqa: ARG002
        return f"[stub:{self.name}] {user[:120]}"


# ----- LLM facade ---------------------------------------------------------


class LLM:
    """Provider with automatic ASI1-Mini fallback."""

    def __init__(self, primary: LLMProvider, fallback: LLMProvider | None = None):
        self.primary = primary
        self.fallback = fallback

    @classmethod
    def from_env(cls) -> "LLM":
        primary: LLMProvider
        if k := os.getenv("ANTHROPIC_API_KEY"):
            primary = AnthropicProvider(k)
        elif k := os.getenv("OPENAI_API_KEY"):
            primary = OpenAIProvider(k)
        elif k := os.getenv("GROQ_API_KEY"):
            primary = GroqProvider(k)
        elif k := os.getenv("ASI1_API_KEY"):
            primary = ASI1MiniProvider(k)
        else:
            primary = StubProvider()

        fallback: LLMProvider | None = None
        if (k := os.getenv("ASI1_API_KEY")) and primary.name != "asi1-mini":
            fallback = ASI1MiniProvider(k)
        return cls(primary, fallback)

    async def complete(self, system: str, user: str, **kw: Any) -> str:
        try:
            return await self.primary.complete(system, user, **kw)
        except Exception as e:
            log.warning("primary LLM %s failed: %s; falling back", self.primary.name, e)
            if self.fallback:
                return await self.fallback.complete(system, user, **kw)
            raise


# ----- Agent base ---------------------------------------------------------


class Agent(abc.ABC):
    """Base class for swarm agents.

    Each agent reads from + writes to the shared `AgentContext`. Agents do not
    call each other directly — the orchestrator owns routing.
    """

    name: str = "agent"

    def __init__(self, llm: LLM | None = None):
        self.llm = llm or LLM.from_env()

    @abc.abstractmethod
    async def run(self, ctx: AgentContext) -> AgentContext: ...

    def _emit(self, ctx: AgentContext, intent: str, payload: dict[str, Any]) -> None:
        ctx.trace.append(
            AgentMessage(sender=self.name, recipient="orchestrator", intent=intent, payload=payload)
        )
