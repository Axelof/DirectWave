from pathlib import Path
from typing import Type

from pydantic import BaseModel

from utils.files import FileMetrics


class FileCache(FileMetrics):
    """
    Класс для кеширования данных из файла

    Args:
        path (Path): путь к файлу на диске
    """

    def __init__(self, path: Path, *, model: Type[BaseModel]):
        super().__init__(path)

        self.model = model
        self.data = self._read_as_model()

    def _read_as_model(self) -> Type[BaseModel]:
        """Чтение данных из файла и преобразование их в указанную модель."""
        return self.model(**self._read()) # noqa

    def get(self):
        """
        Получает данные, обновляя их при необходимости
        """
        if not self.is_actually:
            self.data = self._read_as_model()
            self.changed = self.edited_at

        return self.data # noqa

    def update(self, *, data: Type[BaseModel]) -> None:
        """
        Обновляет данные объекта, сохраняя их в файле на диске
        """
        self._write(data.dict()) # noqa
        self.data = data
        self.changed = self.edited_at
