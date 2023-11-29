import time

from pydantic import BaseModel, Field

from enums.jwt import TokenType, Scopes


class TokenPayload(BaseModel):
    type: TokenType = Field(...)
    sub: str = Field(...)
    iss: str = Field(...)

    iat: float = Field(default_factory=lambda: time.time())


class ExtendedTokenPayload(TokenPayload):
    scopes: list[Scopes] = Field(...)
    id: int = Field(...)


class VerifyTokenPayload(TokenPayload):
    exp: float = Field(default_factory=lambda: time.time() + 604800)
    type: TokenType = Field(default=TokenType.VERIFY)


class AccessTokenPayload(ExtendedTokenPayload):
    exp: float = Field(default_factory=lambda: time.time() + 3600)
    type: TokenType = Field(default=TokenType.ACCESS)


class RefreshTokenPayload(ExtendedTokenPayload):
    exp: float = Field(default_factory=lambda: time.time() + 86400)
    nbf: float = Field(default_factory=lambda: time.time() + 3600)
    type: TokenType = Field(default=TokenType.REFRESH)



