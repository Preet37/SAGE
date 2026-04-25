"""
Base classes for SAGE Fetch.ai uAgents.
All agents implement the Chat Protocol and use ASI1-Mini for reasoning.
"""
import os
from openai import AsyncOpenAI
from app.config import get_settings

settings = get_settings()


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
