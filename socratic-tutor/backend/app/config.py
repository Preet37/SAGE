"""Application settings — loads config from settings.yaml + secrets from .env."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml
from dotenv import load_dotenv

_BACKEND_DIR = Path(__file__).parent.parent
_SETTINGS_PATH = _BACKEND_DIR / "settings.yaml"

CONTENT_DIR: Path = Path(
    os.environ.get("CONTENT_DIR", str(_BACKEND_DIR.parent / "content"))
).resolve()
WIKI_DIR: Path = CONTENT_DIR / "pedagogy-wiki"


def _load_yaml() -> dict:
    with open(_SETTINGS_PATH) as f:
        return yaml.safe_load(f)


class Settings:
    def __init__(self) -> None:
        load_dotenv(_BACKEND_DIR / ".env")
        cfg = _load_yaml()

        # Database
        self.database_url: str = cfg["database"]["url"]

        # Secrets from .env only
        self.llm_api_key: str = os.getenv("LLM_API_KEY", "")

        jwt_secret = os.getenv("JWT_SECRET", "")
        if not jwt_secret:
            raise RuntimeError(
                "JWT_SECRET environment variable is not set. "
                "Generate one with: python -c \"import secrets; print(secrets.token_urlsafe(64))\""
            )
        self.jwt_secret: str = jwt_secret

        # LLM provider (any OpenAI-compatible API)
        self.llm_base_url: str = cfg["llm"]["base_url"]

        # Search (optional — only active when SEARCH_API_KEY is set)
        self.search_api_key: str = os.getenv("SEARCH_API_KEY", "")
        self.search_base_url: str = cfg.get("search", {}).get("base_url", "")

        # Tutor model
        tutor = cfg["models"]["tutor"]
        self.llm_model: str = tutor["model_id"]
        self.llm_max_tokens: int = tutor["max_tokens"]
        self.llm_temperature: float = tutor["temperature"]

        # Vision model (optional, for multimodal image annotation)
        vision = cfg.get("models", {}).get("vision", {})
        self.vision_llm_model: str | None = vision.get("model_id")

        # Fallback model (optional, used when primary model times out)
        fallback = cfg.get("models", {}).get("fallback", {})
        self.fallback_llm_model: str | None = fallback.get("model_id")

        # Fast model (lightweight tasks: summarization, card extraction)
        fast = cfg.get("models", {}).get("fast", {})
        self.fast_llm_model: str | None = fast.get("model_id")

        # Rerank model (optional, falls back to tutor model)
        rerank = cfg.get("models", {}).get("rerank", {})
        self.rerank_model: str | None = rerank.get("model_id")

        # Usage limits
        usage = cfg.get("usage", {})
        self.daily_message_limit: int = usage.get("daily_messages", 0)

        # Auth
        auth = cfg["auth"]
        self.jwt_algorithm: str = auth["jwt_algorithm"]
        self.jwt_expire_minutes: int = auth["jwt_expire_minutes"]

        # Server — env var overrides settings.yaml for containerized deploys
        self.frontend_url: str = os.getenv(
            "FRONTEND_URL", cfg["server"]["frontend_url"]
        )

    @property
    def search_enabled(self) -> bool:
        has_perplexity = bool(self.search_api_key and self.search_base_url)
        has_nvidia = bool(self.llm_api_key and self.llm_base_url)
        return has_perplexity or has_nvidia


@lru_cache
def get_settings() -> Settings:
    return Settings()
