from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Populate os.environ from .env so direct os.getenv(...) calls in agent code
# (which use ANTHROPIC_API_KEY / ASI1_API_KEY) see the configured values.
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./sage.db"
    jwt_secret: str = "change-me-in-prod"
    jwt_alg: str = "HS256"
    jwt_expire_minutes: int = 60 * 24


settings = Settings()
