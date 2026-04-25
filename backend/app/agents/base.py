"""
Base classes for SAGE Fetch.ai uAgents.
All agents implement the Chat Protocol and use ASI1-Mini for reasoning.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Optional, Protocol

from openai import AsyncOpenAI
from app.config import get_settings

settings = get_settings()


@dataclass
class AgentMessage:
    sender: str
    receiver: str
    kind: str
    payload: dict[str, Any]


@dataclass
class AgentContext:
    session_id: int
    user_id: int
    user_message: str
    sources: list[str] = field(default_factory=list)
    mastery: list[dict[str, Any]] = field(default_factory=list)
    a11y: dict[str, Any] = field(default_factory=dict)
    plan: dict[str, Any] = field(default_factory=dict)
    answer: str = ""
    verification: dict[str, Any] = field(default_factory=dict)
    concept_map_delta: list[dict[str, Any]] = field(default_factory=list)
    assessment: dict[str, Any] = field(default_factory=dict)
    peers: list[dict[str, Any]] = field(default_factory=list)
    progress_delta: dict[str, Any] = field(default_factory=dict)
    trace: list[AgentMessage] = field(default_factory=list)
    db: Optional[Any] = None  # AsyncSession injected by orchestrator for DB-backed agents


class Provider(Protocol):
    name: str

    async def complete(self, system: str, user: str, max_tokens: int = 512) -> str:
        ...


class StubProvider:
    name = "stub"

    async def complete(self, system: str, user: str, max_tokens: int = 512) -> str:
        return f"[stub:{self.name}] {user[:120]}"


class OpenAIProvider:
    name = "openai-compatible"

    def __init__(self, client: AsyncOpenAI, model: str):
        self.client = client
        self.model = model

    async def complete(self, system: str, user: str, max_tokens: int = 512) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""


class LLM:
    def __init__(self, primary: Provider | None = None, fallback: Provider | None = None):
        self.primary = primary or StubProvider()
        self.fallback = fallback

    @classmethod
    def from_env(cls) -> "LLM":
        if settings.asi1_api_key:
            client = AsyncOpenAI(base_url="https://api.asi1.ai/v1", api_key=settings.asi1_api_key)
            return cls(OpenAIProvider(client, "asi1-mini"), StubProvider())
        if settings.llm_provider in {"openai", "groq"} and settings.llm_api_key:
            base_url = (
                "https://api.groq.com/openai/v1"
                if settings.llm_provider == "groq"
                else "https://api.openai.com/v1"
            )
            model = "llama-3.1-8b-instant" if settings.llm_provider == "groq" else "gpt-4o"
            client = AsyncOpenAI(base_url=base_url, api_key=settings.llm_api_key)
            return cls(OpenAIProvider(client, model), StubProvider())
        return cls(StubProvider())

    async def complete(self, system: str, user: str, max_tokens: int = 512) -> str:
        try:
            return await self.primary.complete(system, user, max_tokens=max_tokens)
        except Exception:
            if self.fallback:
                return await self.fallback.complete(system, user, max_tokens=max_tokens)
            raise


class Agent:
    name = "agent"

    def __init__(self, llm: LLM | None = None):
        self.llm = llm or LLM.from_env()

    def _emit(self, ctx: AgentContext, kind: str, payload: dict[str, Any]) -> None:
        ctx.trace.append(AgentMessage(self.name, "orchestrator", kind, payload))

    async def run(self, ctx: AgentContext) -> AgentContext:
        raise NotImplementedError


def get_agent_client() -> AsyncOpenAI:
    """
    Returns the best available LLM client for agent reasoning.
    Prefers ASI1-Mini (Fetch.ai track), falls back to Groq, then OpenAI.
    """
    if settings.asi1_api_key and settings.asi1_api_key != settings.agentverse_api_key:
        return AsyncOpenAI(base_url="https://api.asi1.ai/v1", api_key=settings.asi1_api_key)
    if settings.llm_provider == "groq":
        return AsyncOpenAI(base_url="https://api.groq.com/openai/v1", api_key=settings.llm_api_key)
    return AsyncOpenAI(base_url="https://api.openai.com/v1", api_key=settings.llm_api_key)


def get_agent_model() -> str:
    if settings.llm_provider == "groq":
        return "llama-3.1-8b-instant"  # fast, cheap for agent calls
    return "asi1-mini"


async def asi1_complete(prompt: str, system: str = "", max_tokens: int = 512) -> str:
    """Single fast completion for agent reasoning."""
    client = get_agent_client()
    model = get_agent_model()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return f"Agent LLM error: {str(e)}"
