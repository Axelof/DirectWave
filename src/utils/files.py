import os
from pathlib import Path
from typing import Any

import orjson
import aiofiles


class File:
    def __init__(self, path: Path):
        self.path = path

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.path}")'

    async def read(self) -> Any:
        async with aiofiles.open(self.path, mode="r", encoding="UTF-8") as file:
            return file.read()

    async def write(self, data: Any) -> None:
        async with aiofiles.open(self.path, mode="w", encoding="UTF-8") as file:
            await file.write(data)

    async def add(self, data: Any) -> None:
        async with aiofiles.open(self.path, mode="a", encoding="UTF-8") as file:
            await file.write(data)

    async def json(self):
        return orjson.loads(await self.read())


class FileMetrics(File):
    def __init__(self, path: Path):
        super().__init__(path)

        self.changed = self.edited_at

    @property
    def edited_at(self) -> float:
        return os.stat(self.path).st_mtime

    @property
    def actually(self) -> bool:
        return self.changed == self.edited_at
