from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="backend/.env", extra="ignore")

    database_url: str = "sqlite:///./sage.db"
    jwt_secret: str = "change-me-in-prod"
    jwt_alg: str = "HS256"
    jwt_expire_minutes: int = 60 * 24
    
    # AI Keys
    gemini_api_key: str | None = None
    anthropic_api_key: str | None = None
    asi1_api_key: str | None = None
    cloudinary_url: str | None = None
    stitch_api_key: str | None = None


settings = Settings()

# Debug: confirm keys are loaded
print(f"--- SAGE CONFIG LOADED ---")
print(f"Database: {settings.database_url}")
print(f"Gemini Key: {'LOADED' if settings.gemini_api_key else 'MISSING'}")
print(f"Anthropic Key: {'LOADED' if settings.anthropic_api_key else 'MISSING'}")
print(f"ASI-1 (Fetch.ai) Key: {'LOADED' if settings.asi1_api_key else 'MISSING'}")
print(f"Cloudinary: {'LOADED' if settings.cloudinary_url else 'MISSING'}")
print(f"--------------------------")
