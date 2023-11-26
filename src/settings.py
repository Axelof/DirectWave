from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_DIR: Path
    PROJECT_NAME: str

    DEBUG: bool
    DOMAIN: str | None


settings = Settings()
