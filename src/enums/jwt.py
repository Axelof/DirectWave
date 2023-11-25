from enum import auto

from src.enums import NameEnum


class TokenType(NameEnum):
    ACCESS = auto()
    REFRESH = auto()


class Scopes(NameEnum):
    MESSAGES = auto()
    FRIENDS = auto()
    PROFILE = auto()
    STATUS = auto()
    EMAIL = auto()
    WALL = auto()


