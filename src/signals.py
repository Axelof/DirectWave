import inspect
import logging
from enum import Enum
from glob import glob
import importlib.util
from pathlib import Path
from asyncio import to_thread
from typing import Callable, List, Tuple

Function = Callable
FunctionsList = List[Tuple[str, str, Function]]


class FunctionLogType(str, Enum):
    STARTUP = "startup"
    SHUTDOWN = "shutdown"


def path_to_module(path: Path) -> str:
    return path.with_suffix("").as_posix().replace("/", ".")


class WatchSignals:
    __slots__ = ["exclude", "functions_on_startup", "functions_on_shutdown"]

    def __init__(self, exclude: list[Path | str] = None):
        self.exclude = exclude or [Path("signals.py")]

        self.functions_on_startup: FunctionsList = []
        self.functions_on_shutdown: FunctionsList = []

        self.get_signals()

    def get_signals(self):
        paths = [Path(signal) for signal in glob("**/signals.py", recursive=True)]
        paths = [path_to_module(path) for path in paths if path not in self.exclude]
        modules = [importlib.import_module(path) for path in paths]

        for module in modules:
            for attributes in dir(module):
                if callable(function := getattr(module, attributes)):
                    if function.__name__.startswith("sp_"):
                        self.functions_on_startup.append((module.__name__, function.__name__[3:], function))
                    if function.__name__.startswith("sn_"):
                        self.functions_on_shutdown.append((module.__name__, function.__name__[3:], function))

    @staticmethod
    async def execute(function: Function):
        if inspect.iscoroutinefunction(function):
            return await function()
        return await to_thread(function)

    @staticmethod
    def log(f_type: FunctionLogType, m_name: str, f_name: str, r: str):
        logging.info(
            "({m_name}) {f_type}_function {f_name}: {r}".format(
                f_type=f_type.value,
                m_name=m_name,
                f_name=f_name,
                r=r,
            )
        )

    async def on_startup(self):
        for module_name, function_name, function in self.functions_on_startup:
            result = await self.execute(function)
            self.log(FunctionLogType.STARTUP, m_name=module_name, f_name=function_name, r=result)

    async def on_shutdown(self):
        for module_name, function_name, function in self.functions_on_shutdown:
            result = await self.execute(function)
            self.log(FunctionLogType.SHUTDOWN, m_name=module_name, f_name=function_name, r=result)

