from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "localhost"
    ai_client_url: str 
    api_key: str 
    model_name: str

    # Load from .env file by default
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Instantiate once to load and validate everything on startup
settings = Settings()