import os
import json
from pathlib import Path
from typing import Type, Any

from pydantic import BaseModel


class File:
    def __init__(self, path: Path):
        self.path = path

    def __repr__(self):
        return f"{self.__class__.__name__}(\"{self.path}\")"

    def read(self) -> Any:
        with open(self.path, mode="r", encoding="UTF-8") as file:
            return file.read()

    def write(self, data: dict) -> None:
        with open(self.path, mode="w", encoding="UTF-8") as file:
            file.write(json.dumps(data, indent=4))


class FileMetrics(File):
    def __init__(self, path: Path):
        super().__init__(path)
        self.changed = self.edited_at

    @property
    def edited_at(self) -> float:
        return os.stat(self.path).st_mtime

    @property
    def is_actually(self) -> bool:
        return self.changed == self.edited_at


class FileCache(FileMetrics):
    """
    Класс для кеширования данных из файла

    Args:
        path (Path): путь к файлу на диске
    """

    def __init__(self, path: Path):
        super().__init__(path)
        self.data = self.read()

    def get(self, *, model: Type[BaseModel] = dict) -> Type[BaseModel] | dict:
        """
        Получает данные, обновляя их при необходимости

        Parameters:
            model (Type[BaseModel]): ожидаемый тип данных (pydantic модель)


        Returns:
            Type[BaseModel] | dict: Данные в виде указанной модели
        """

        if not self.is_actually:
            self.data = self.read()
            self.changed = self.edited_at

        if model is dict:
            return self.data
        return model(**self.data)  # noqa

    def update(self, *, data: Type[BaseModel] | dict) -> None:
        """
        Обновляет данные объекта, сохраняя их в файле на диске

            Если переданные данные являются экземпляром pydantic-модели, они преобразуются
            в словарь с использованием метода `dict()` перед сохранением

        Parameters:
            data (Type[BaseModel] | dict): данные для обновления
        """
        if isinstance(data, BaseModel):
            data = data.dict()

        self.write(data)
        self.data = data
        self.changed = self.edited_at
