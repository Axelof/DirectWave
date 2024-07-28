import contextlib
from functools import partial

import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from utils.files import File
from definitions import FILES_DIR
from enums.jwt import TokenType, Scopes
from utils.encoders import CustomJsonEncoder
from JWT.models import (
    TokenPayload,
    AccessTokenPayload,
    RefreshTokenPayload,
    VerifyTokenPayload,
)


class Sign:
    # Follow the RFC: https://datatracker.ietf.org/doc/html/rfc7519
    def __init__(self, jwt_bearer: "JWTBearer"):
        self.jwt = jwt_bearer

    def verify(self, jti: str, email: str):
        return self.jwt.encode(
            VerifyTokenPayload(
                jti=jti, iss=JWTBearer.ISSUER, sub=JWTBearer.SUBJECT
            ).dict()
        )

    def access(self, jti: str, _id: str, scopes: list[Scopes]):
        return self.jwt.encode(
            AccessTokenPayload(
                jti=jti,
                id=_id,
                scopes=scopes,
                iss=JWTBearer.ISSUER,
                sub=JWTBearer.SUBJECT,
            ).dict()
        )

    def refresh(self, jti: str, _id: str, scopes: list[Scopes]):
        return self.jwt.encode(
            RefreshTokenPayload(
                jti=jti,
                id=_id,
                scopes=scopes,
                iss=JWTBearer.ISSUER,
                sub=JWTBearer.SUBJECT,
            ).dict()
        )


class Blacklist:
    def __init__(self, jwt_bearer: "JWTBearer"):
        self.jwt = jwt_bearer
        self.file = File(FILES_DIR / "jwt" / "blacklist.json")

    def _in(self, jti: str):
        pass

    def add(self, jti: str):
        pass


class JWTBearer(HTTPBearer):
    ISSUER = "DirectWave"
    SUBJECT = "DW (API)"

    def __init__(
        self,
        _type: TokenType,
        secret: str,
        auto_error: bool = True,
        algorithm: str = "HS256",
    ):
        self.type = _type

        self.encode = partial(
            jwt.encode,
            key=secret,
            algorithm=algorithm,
            json_encoder=CustomJsonEncoder,
        )

        self.decode = partial(jwt.decode, key=secret, algorithms=[algorithm])

        self.sign = Sign(self)

        super().__init__(auto_error=auto_error)

    async def __call__(self, _: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(_)

        if not await self.verify(credentials):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="403 Forbidden. Access denied",
            )

        return credentials.credentials

    async def verify(self, credentials: HTTPAuthorizationCredentials):
        decrypted_payload = await self.decrypt(credentials.credentials)

        with contextlib.suppress(AttributeError):
            return decrypted_payload.type == self.type
        return False

    async def decrypt(
        self, token: str
    ) -> AccessTokenPayload | RefreshTokenPayload | VerifyTokenPayload | None:
        with contextlib.suppress(DecodeError, ExpiredSignatureError):
            unprocessed_payload = self.decode(jwt=token)
            payload = TokenPayload(**unprocessed_payload)

            match payload.type:
                case TokenType.ACCESS:
                    payload = AccessTokenPayload(**unprocessed_payload)
                case TokenType.REFRESH:
                    payload = RefreshTokenPayload(**unprocessed_payload)
                case TokenType.VERIFY:
                    payload = VerifyTokenPayload(**unprocessed_payload)
                case _:
                    payload = None

            return payload

        return None  # TODO: реализовать запись ошибки в лог-файлы
