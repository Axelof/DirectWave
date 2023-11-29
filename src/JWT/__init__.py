from JWT.handler import JWTBearer
from settings import settings

JWT = JWTBearer(secret=settings.SECRET)
