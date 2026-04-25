"""
Base classes for SAGE Fetch.ai uAgents.
All agents implement the Chat Protocol and use ASI1-Mini for reasoning.
"""
import os
from openai import AsyncOpenAI
from app.config import get_settings

settings = get_settings()


def get_asi1_client() -> AsyncOpenAI:
    """ASI1-Mini client via OpenAI-compatible API."""
    return AsyncOpenAI(
        base_url="https://api.asi1.ai/v1",
        api_key=settings.asi1_api_key or settings.llm_api_key,
    )


async def asi1_complete(prompt: str, system: str = "", max_tokens: int = 512) -> str:
    """Single completion via ASI1-Mini."""
    client = get_asi1_client()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        response = await client.chat.completions.create(
            model="asi1-mini",
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return f"ASI1 error: {str(e)}"
