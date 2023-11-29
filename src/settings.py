from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_DIR: Path

    PROJECT_NAME: str
    DEBUG: bool
    DOMAIN: str | None

    SECRET: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str


settings = Settings()
