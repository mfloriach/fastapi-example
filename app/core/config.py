from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AWS_REGION: str
    AWS_COGNITO_APP_CLIENT_ID: str
    AWS_COGNITO_APP_CLIENT_SECRET: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    JWKS_URL: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

@lru_cache
def get_settings():
    return settings

env_vars = get_settings()