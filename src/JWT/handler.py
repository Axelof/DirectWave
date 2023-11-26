import contextlib
import secrets

import jwt
from jwt.exceptions import DecodeError

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from JWT.models import TokenPayload, AccessTokenPayload, RefreshTokenPayload
from enums.jwt import TokenType, Scopes
from utils.encoders import CustomJsonEncoder


class JWTBearer(HTTPBearer):
    def __init__(
            self,
            secret: str,
            auto_error: bool = True,
            algorithm: str = "HS256"
    ):
        self.secret = secret
        self.algorithm = algorithm

        super().__init__(auto_error=auto_error)

    async def __call__(self, _: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(_)

        if not await self.verify(credentials):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="403 Forbidden. Access denied."
            )

        return credentials.credentials

    def sign(self, _id: int, scopes: Scopes | list[Scopes]):
        payload = {
            "scopes": scopes if type(scopes) == list else [scopes],
            "jti": secrets.token_hex(16),
            "iss": "DirectWave (DW)",
            "sub": "DW (API)",
            "id": _id
        }

        access_token = AccessTokenPayload(**payload)
        refresh_token = RefreshTokenPayload(**payload)

        return {
            "access_token": jwt.encode(
                access_token.dict(), json_encoder=CustomJsonEncoder,
                algorithm=self.algorithm, key=self.secret
            ),

            "refresh_token": jwt.encode(
                refresh_token.dict(), json_encoder=CustomJsonEncoder,
                algorithm=self.algorithm, key=self.secret
            )
        }

    async def decrypt(self, token: str) -> AccessTokenPayload | RefreshTokenPayload | None:
        with contextlib.suppress(DecodeError):
            raw_payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            payload = TokenPayload(**raw_payload)

            if payload.type == TokenType.ACCESS:
                return AccessTokenPayload(**raw_payload)
            return RefreshTokenPayload(**raw_payload)

        return None  # TODO: реализовать запись ошибки в лог-файлы.

    async def verify(self, credentials: HTTPAuthorizationCredentials):
        return True if await self.decrypt(credentials.credentials) else False
