"""Voice synthesis — ElevenLabs with browser TTS fallback."""
import httpx
from typing import Optional, AsyncGenerator
from app.config import get_settings

settings = get_settings()


async def synthesize_speech(text: str) -> Optional[bytes]:
    """
    Synthesize text to speech using ElevenLabs.
    Returns MP3 bytes, or None if ElevenLabs is not configured.
    """
    if not settings.elevenlabs_api_key:
        return None

    clean_text = _clean_for_tts(text)
    if not clean_text:
        return None

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{settings.elevenlabs_voice_id}"
    headers = {
        "xi-api-key": settings.elevenlabs_api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": clean_text[:2500],
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.content
    except Exception:
        return None


def _clean_for_tts(text: str) -> str:
    """Remove markdown and code blocks for cleaner TTS output."""
    import re
    text = re.sub(r"```[\s\S]*?```", "[code block]", text)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"#{1,6}\s", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:2500]
