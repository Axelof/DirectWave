from functools import partial

from JWT.handler import JWTBearer
from settings import settings

JWT = partial(JWTBearer, secret=settings.project.secret)
