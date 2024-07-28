import logging
import sys
from types import FrameType
from typing import cast

import logfire
from loguru import logger

from settings import settings

LEVEL = logging.DEBUG if settings.debug else logging.INFO
DATETIME_FORMAT = "DD.MM.YYYY HH^mm (ss)"
LOGGER_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<red><level>{level: <8}</level></red> | "
    "<cyan>{name}:{function}:{line}</cyan> | "
    "{message}"
)


def configure_logging():
    logger.remove()
    logger.add(
        sys.stdout,
        level=LEVEL,
        format=LOGGER_FORMAT,
        backtrace=False,
    )

    # configure file logging
    logger.add(
        f"logs/{{time:{DATETIME_FORMAT}}}.log",
        rotation="4 MB",
        compression="zip",
    )

    # handle all default logging
    logging.basicConfig(
        level=logging.INFO,
        force=True,
        handlers=[InterceptHandler(), logfire.LogfireLoggingHandler()],
    )

    # configure default logging
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    # configure logfire (https://docs.pydantic.dev/logfire/)
    logfire.configure(
        console=False,
        send_to_logfire=True,
        pydantic_plugin=logfire.PydanticPlugin(record="all"),
        token=settings.logfire.token.get_secret_value(),
        service_name=settings.project.name,
        service_version=settings.project.version,
    )


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        frame, depth = logging.currentframe(), 0

        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame, depth = cast(FrameType, frame.f_back), depth + 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )
