from enum import Enum


class NameEnum(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    @property
    def locale_ids(self) -> dict[Enum, str]:
        raise NotImplementedError()

    # @property
    # def localized(self) -> str:
    #     return gettext(self.locale_ids[self])


class ListEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
