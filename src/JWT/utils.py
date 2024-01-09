from datetime import datetime

from pydantic import BaseModel

from JWT.models import TokenPayload
from definitions import FILES_DIR
from enums.jwt import TokenType
from utils.cache import FileCache


path = FILES_DIR / "files" / "blacklist.json"


class BlacklistObjectModel(BaseModel):
    type: TokenType
    jti: str
    exp: datetime
    description: str | None


class BlacklistModel(BaseModel):
    list: list[BlacklistObjectModel]


class Blacklist(FileCache):
    def __init__(self):
        self.data: BlacklistModel = self.data
        super().__init__(path, model=BlacklistModel)

    def add(self, token: TokenPayload, description: str = None):
        self.data.list.append()

    def is_blacklisted(self, token: TokenPayload):
        return any(item.jti == token.jti for item in self.get())


blacklist = Blacklist()
