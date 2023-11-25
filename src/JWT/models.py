import secrets
import time

from pydantic import BaseModel, Field

from src.enums.jwt import TokenType, Scopes


class TokenPayload(BaseModel):
    scopes: list[Scopes] = Field(...)
    type: TokenType = Field(...)
    sub: str = Field(...)
    iss: str = Field(...)
    id: int = Field(...)

    iat: float = Field(default_factory=lambda: time.time())


class AccessTokenPayload(TokenPayload):
    exp: float = Field(default_factory=lambda: time.time() + 3600)
    type: TokenType = Field(default=TokenType.ACCESS)


class RefreshTokenPayload(TokenPayload):
    exp: float = Field(default_factory=lambda: time.time() + 86400)
    nbf: float = Field(default_factory=lambda: time.time() + 3600)
    type: TokenType = Field(default=TokenType.REFRESH)
