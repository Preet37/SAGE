from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Populate os.environ from .env so direct os.getenv(...) calls in agent code
# (which use ANTHROPIC_API_KEY / ASI1_API_KEY / etc.) see the configured values.
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./sage.db"
    jwt_secret: str = "change-me-in-prod"
    jwt_alg: str = "HS256"
    jwt_expire_minutes: int = 60 * 24

    environment: str = "development"  # "development" | "production"
    log_level: str = "INFO"

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


settings = Settings()


def assert_safe_for_production() -> None:
    """Raise if production deployment is using insecure defaults."""
    if not settings.is_production:
        return
    if settings.jwt_secret == "change-me-in-prod" or len(settings.jwt_secret) < 32:
        raise RuntimeError(
            "JWT_SECRET must be a 32+ character random string in production."
        )
    if settings.database_url.startswith("sqlite"):
        raise RuntimeError(
            "Set DATABASE_URL to a Postgres URL in production; SQLite is dev-only."
        )
