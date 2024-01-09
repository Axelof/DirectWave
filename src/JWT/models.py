from datetime import datetime, timedelta

from pydantic import BaseModel, Field


from enums.jwt import TokenType, Scopes


class TokenPayload(BaseModel):
    type: TokenType = Field(...)
    sub: str = Field(...)
    iss: str = Field(...)
    jti: str = Field(...)
    exp: datetime

    iat: datetime = Field(default_factory=lambda: datetime.timestamp(datetime.now()))

    @property
    def is_blacklisted(self):
        from JWT.utils import blacklist
        return blacklist.is_blacklisted(self.jti)


class UserPayload(BaseModel):
    scopes: list[Scopes] = Field(...)
    id: int = Field(...)


class VerifyTokenPayload(TokenPayload):
    exp: datetime = Field(default_factory=lambda: datetime.now() + timedelta(seconds=604800))
    type: TokenType = Field(default=TokenType.VERIFY)


class AccessTokenPayload(TokenPayload, UserPayload):
    exp: datetime = Field(default_factory=lambda: datetime.now() + timedelta(seconds=3600))
    type: TokenType = Field(default=TokenType.ACCESS)


class RefreshTokenPayload(TokenPayload, UserPayload):
    exp: datetime = Field(default_factory=lambda: datetime.now() + timedelta(seconds=86400))
    nbf: datetime = Field(default_factory=lambda: datetime.now() + timedelta(seconds=3600))
    type: TokenType = Field(default=TokenType.REFRESH)
