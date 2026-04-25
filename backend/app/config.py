from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./sage.db"
    jwt_secret: str = "change-me-in-prod"
    jwt_alg: str = "HS256"
    jwt_expire_minutes: int = 60 * 24


settings = Settings()
