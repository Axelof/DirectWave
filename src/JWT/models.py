import time

from pydantic import BaseModel, Field


from enums.jwt import TokenType, Scopes


class TokenPayload(BaseModel):
    type: TokenType = Field(...)
    sub: str = Field(...)
    iss: str = Field(...)
    jti: str = Field(...)
    exp: float

    iat: float = Field(default_factory=lambda: time.time())

    @property
    def is_blacklisted(self):
        return NotImplemented
        # TODO: Pseudo-code
        # from JWT.utils import blacklist
        # return blacklist.in(self.jti)


class UserPayload(BaseModel):
    scopes: list[Scopes] = Field(...)
    id: int = Field(...)


class VerifyTokenPayload(TokenPayload):
    exp: float = Field(default_factory=lambda: time.time() + 604800)
    type: TokenType = Field(default=TokenType.VERIFY)


class AccessTokenPayload(TokenPayload, UserPayload):
    exp: float = Field(default_factory=lambda: time.time() + 3600)
    type: TokenType = Field(default=TokenType.ACCESS)


class RefreshTokenPayload(TokenPayload, UserPayload):
    exp: float = Field(default_factory=lambda: time.time() + 86400)
    nbf: float = Field(default_factory=lambda: time.time() + 3600)
    type: TokenType = Field(default=TokenType.REFRESH)



