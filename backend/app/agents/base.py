"""Agent base classes + LLM provider abstraction.

Primary provider: Anthropic Claude (when `ANTHROPIC_API_KEY` is set).
Fallback provider: ASI1-Mini via Fetch.ai (`ASI1_API_KEY`), used when Anthropic
is unavailable or returns an error. Both are wrapped behind `LLM.complete()`
so individual agents never know which model answered.
"""

from __future__ import annotations

import abc
import logging
import os
from dataclasses import dataclass, field
from typing import Any, Protocol

import httpx
from google import genai

from app.config import settings
log = logging.getLogger("sage.agents")


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


class LLMProvider(Protocol):
    name: str

    async def complete(self, system: str, user: str, **kw: Any) -> str: ...


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, api_key: str, model: str = "claude-opus-4-7"):
        self.api_key = api_key
        self.model = model

    async def complete(self, system: str, user: str, **kw: Any) -> str:
        async with httpx.AsyncClient(timeout=30.0) as c:
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


class ASI1MiniProvider:
    """Fetch.ai ASI1-Mini fallback."""

    name = "asi1-mini"

    def __init__(self, api_key: str, model: str = "asi1-mini"):
        self.api_key = api_key
        self.model = model

    async def complete(self, system: str, user: str, **kw: Any) -> str:
        async with httpx.AsyncClient(timeout=30.0) as c:
            r = await c.post(
                "https://api.asi1.ai/v1/chat/completions",
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


class GeminiProvider:
    """Google Gemini provider."""

    name = "gemini"

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def complete(self, system: str, user: str, **kw: Any) -> str:
        # Use sync-to-async wrapper if genai doesn't have native async, 
        # or just call it directly if it's fast enough. 
        # Actually, genai.Client().models.generate_content is usually synchronous in this SDK.
        # We'll use asyncio.to_thread to avoid blocking.
        import asyncio
        response = await asyncio.to_thread(
            self.client.models.generate_content,
            model=self.model,
            config={"system_instruction": system},
            contents=user
        )
        return response.text


class StubProvider:
    """Offline default — used when no API keys are configured."""

    name = "stub"

    async def complete(self, system: str, user: str, **kw: Any) -> str:
        return f"[stub:{self.name}] {user[:120]}"


class LLM:
    """Provider with automatic ASI1-Mini fallback."""

    def __init__(self, primary: LLMProvider, fallback: LLMProvider | None = None):
        self.primary = primary
        self.fallback = fallback

    @classmethod
    def from_env(cls) -> "LLM":
        primary: LLMProvider
        if settings.asi1_api_key:
            primary = ASI1MiniProvider(settings.asi1_api_key)
        elif settings.anthropic_api_key:
            primary = AnthropicProvider(settings.anthropic_api_key)
        elif settings.gemini_api_key:
            primary = GeminiProvider(settings.gemini_api_key)
        else:
            primary = StubProvider()

        fallback: LLMProvider | None = None
        if settings.gemini_api_key and primary.name != "gemini":
            fallback = GeminiProvider(settings.gemini_api_key)
        elif settings.asi1_api_key and primary.name != "asi1-mini":
            fallback = ASI1MiniProvider(settings.asi1_api_key)
        return cls(primary, fallback)

    async def complete(self, system: str, user: str, **kw: Any) -> str:
        try:
            return await self.primary.complete(system, user, **kw)
        except Exception as e:
            log.warning("primary LLM %s failed: %s; falling back", self.primary.name, e)
            if self.fallback:
                return await self.fallback.complete(system, user, **kw)
            raise


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
