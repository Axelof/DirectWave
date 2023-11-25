from pydantic import SecretStr

from .handler import JWTBearer


JWT = JWTBearer("mewjab")