"""ElevenLabs text-to-speech with markdown sanitisation.

`synthesize(text)` returns base64-encoded MP3 bytes when both
`ELEVENLABS_API_KEY` and `ELEVENLABS_VOICE_ID` are set; otherwise returns
None. Failures are swallowed (the tutor stream still completes).
"""

from __future__ import annotations

import base64
import logging
import os
import re

import httpx

log = logging.getLogger("sage.voice")

_CODE = re.compile(r"```.*?```", re.DOTALL)
_INLINE = re.compile(r"`([^`]+)`")
_HEADING = re.compile(r"^#+\s*", re.MULTILINE)
_BOLD_IT = re.compile(r"[*_]{1,3}([^*_]+)[*_]{1,3}")
_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_QUIZ = re.compile(r"<quiz>.*?</quiz>", re.DOTALL)


def sanitize_for_speech(md: str) -> str:
    """Strip markdown / quiz blocks so TTS reads natural prose."""
    md = _QUIZ.sub("", md)
    md = _CODE.sub(" code example. ", md)
    md = _INLINE.sub(r"\1", md)
    md = _HEADING.sub("", md)
    md = _BOLD_IT.sub(r"\1", md)
    md = _LINK.sub(r"\1", md)
    return md.strip()


async def synthesize(text: str) -> str | None:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID")
    if not api_key or not voice_id:
        return None
    clean = sanitize_for_speech(text)
    if not clean:
        return None
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    try:
        async with httpx.AsyncClient(timeout=20.0) as c:
            r = await c.post(
                url,
                headers={
                    "xi-api-key": api_key,
                    "accept": "audio/mpeg",
                    "content-type": "application/json",
                },
                json={
                    "text": clean[:4000],
                    "model_id": "eleven_turbo_v2",
                    "voice_settings": {"stability": 0.4, "similarity_boost": 0.75},
                },
            )
            r.raise_for_status()
            return base64.b64encode(r.content).decode("ascii")
    except Exception as e:
        log.warning("eleven labs synthesis failed: %s", e)
        return None
