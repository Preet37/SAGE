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
        # Cloudinary reads CLOUDINARY_URL at module import time, before load_dotenv
        # runs. Re-configure it now that the env is populated.
        if os.getenv("CLOUDINARY_URL"):
            try:
                import cloudinary as _cl
                _cl.reset_config()
            except Exception:
                pass

        cfg = _load_yaml()

        # Database
        self.database_url: str = cfg["database"]["url"]

        # Secrets from .env only — accept LLM_API_KEY or the provider-specific keys
        self.llm_api_key: str = (
            os.getenv("LLM_API_KEY")
            or os.getenv("GROQ_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or os.getenv("ANTHROPIC_API_KEY")
            or ""
        )

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

        # ── Track features ────────────────────────────────────
        features = cfg.get("features", {})
        self.feature_verification: bool = bool(features.get("verification", False))
        self.feature_semantic_memory: bool = bool(features.get("semantic_memory", False))
        self.feature_mcp_server: bool = bool(features.get("mcp_server", False))
        self.feature_peer_network: bool = bool(features.get("peer_network", False))
        self.feature_resource_router: bool = bool(features.get("resource_router", False))
        self.feature_cloudinary: bool = bool(features.get("cloudinary", False))
        self.feature_fetchai_agent: bool = bool(features.get("fetchai_agent", False))
        self.feature_on_device: bool = bool(features.get("on_device", False))

        # Cloudinary
        cl = cfg.get("cloudinary", {})
        self.cloudinary_cloud_name: str = os.getenv(
            "CLOUDINARY_CLOUD_NAME", cl.get("cloud_name", "")
        )
        self.cloudinary_api_key: str = os.getenv("CLOUDINARY_API_KEY", "")
        self.cloudinary_api_secret: str = os.getenv("CLOUDINARY_API_SECRET", "")
        self.cloudinary_upload_preset: str = cl.get("upload_preset", "sage_unsigned")
        self.cloudinary_folder: str = cl.get("folder", "sage")

        # Fetch.ai
        fai = cfg.get("fetchai", {})
        self.fetchai_agentverse_url: str = fai.get(
            "agentverse_url", "https://agentverse.ai"
        )
        self.fetchai_asi_one_url: str = fai.get("asi_one_url", "https://asi1.ai")
        self.fetchai_agent_name: str = fai.get("agent_name", "sage-tutor")
        self.fetchai_agent_seed: str = os.getenv(
            "FETCHAI_AGENT_SEED", fai.get("agent_seed", "")
        )
        self.agentverse_api_key: str = os.getenv("AGENTVERSE_API_KEY", "")

        # Resource router
        rr = cfg.get("resource_router", {})
        self.arxiv_url: str = rr.get("arxiv_url", "http://export.arxiv.org/api/query")
        self.github_url: str = rr.get("github_url", "https://api.github.com")
        self.youtube_api_key: str = os.getenv("YOUTUBE_API_KEY", "")
        self.youtube_search_enabled: bool = bool(rr.get("youtube_search_enabled", False))

        # Twilio SMS integration (optional — mock mode when absent)
        self.twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
        self.twilio_phone_number: str = os.getenv("TWILIO_PHONE_NUMBER", "")

    @property
    def search_enabled(self) -> bool:
        has_perplexity = bool(self.search_api_key and self.search_base_url)
        has_nvidia = bool(self.llm_api_key and self.llm_base_url)
        return has_perplexity or has_nvidia


@lru_cache
def get_settings() -> Settings:
    return Settings()
