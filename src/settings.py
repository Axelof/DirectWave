from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class ProjectSettings(BaseSettings):
    name: str
    version: str
    domain: str
    dir: Path
    secret: SecretStr

    @property
    def callback_url(self):
        return f"https://{self.domain}/callback"

    class Config:
        env_prefix = "project_"


class LogfireSettings(BaseSettings):
    token: SecretStr

    class Config:
        env_prefix = "logfire_"


class RedisSettings(BaseSettings):
    host: str
    port: int

    class Config:
        env_prefix = "redis_"


class MailSettings(BaseSettings):
    host: str
    port: int
    username: str
    password: str

    class Config:
        env_prefix = "mail_"


class Settings(BaseSettings):
    debug: bool

    project: ProjectSettings = ProjectSettings()
    logfire: LogfireSettings = LogfireSettings()
    redis: RedisSettings = RedisSettings()
    mail: MailSettings = MailSettings()


settings = Settings()
