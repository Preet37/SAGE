from functools import lru_cache
import os
from pathlib import Path
import yaml
from dotenv import load_dotenv
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Populate os.environ from .env so direct os.getenv(...) calls in agent code
# (which use ANTHROPIC_API_KEY / ASI1_API_KEY / etc.) see the configured values.
load_dotenv()


class Settings(BaseSettings):
    # LLM
    llm_api_key: str = Field(
        default="",
        validation_alias=AliasChoices(
            "LLM_API_KEY",
            "ANTHROPIC_API_KEY",
            "OPENAI_API_KEY",
            "GROQ_API_KEY",
        ),
    )
    llm_provider: str = "anthropic"

    # Fetch.ai
    agentverse_api_key: str = ""
    asi1_api_key: str = ""

    # Auth
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"

    # Database
    database_url: str = "sqlite+aiosqlite:///./sage.db"

    # Voice
    elevenlabs_api_key: str = ""
    elevenlabs_voice_id: str = "21m00Tcm4TlvDq8ikWAM"

    # Search
    search_api_key: str = ""

    # Server
    frontend_url: str = "http://localhost:3000"
    cors_extra_origins: str = ""
    backend_port: int = 8000
    content_dir: str = "./content"

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"  # "development" | "production"
    log_level: str = "INFO"

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    if not os.getenv("LLM_PROVIDER"):
        if os.getenv("ASI1_API_KEY") and not s.llm_api_key:
            s.llm_provider = "asi1"
        elif os.getenv("GROQ_API_KEY"):
            s.llm_provider = "groq"
        elif os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
            s.llm_provider = "openai"
    return s


def load_yaml_config() -> dict:
    config_path = Path(__file__).parent.parent / "settings.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def get_tutor_model(settings: Settings, yaml_cfg: dict) -> str:
    provider = settings.llm_provider
    models = yaml_cfg.get("models", {}).get("tutor", {})
    return models.get(provider, "claude-sonnet-4-5")


def get_judge_model(settings: Settings, yaml_cfg: dict) -> str:
    provider = settings.llm_provider
    models = yaml_cfg.get("models", {}).get("judge", {})
    return models.get(provider, "claude-haiku-3-5")
