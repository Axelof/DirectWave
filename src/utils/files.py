import os
import json
from pathlib import Path
from typing import Type, Any

from pydantic import BaseModel


class File:
    def __init__(self, path: Path):
        self.path = path

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.path}")'

    def _read(self) -> Any:
        with open(self.path, mode="r", encoding="UTF-8") as file:
            return file.read()

    def _write(self, data: dict) -> None:
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
