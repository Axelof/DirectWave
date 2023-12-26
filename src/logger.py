import re
import sys
import logging

from loguru import logger

from settings import settings

_logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<red><level>{level: <8}</level></red> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "{message}"
)


_loggers_whitelist = [
    r"tortoise",
    r"fastapi",
    # r'apscheduler',
]


_logger_blacklist = [r"apscheduler"]


_logs_regex_blacklist = []

_logger = logger


def hide_secrets(record: dict):
    record["message"] = record["message"].replace(settings.SECRET, "[SECRET]")
    record["message"] = record["message"].replace(settings.EMAIL_PASSWORD, "[PASSWORD]")


def filter_logs(record: dict):
    return not any(
        re.match(regex, record["message"]) for regex in _logs_regex_blacklist
    )


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists.
        try:
            level = _logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame = logging.currentframe()
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back

        _logger.opt(depth=1, exception=record.exc_info).log(level, record.getMessage())


class WhitelistLoggerDict(dict):
    def __setitem__(self, name, logger_instance):
        enable = any(re.match(regex, name) for regex in _loggers_whitelist)
        logger_instance.disabled = not enable
        logger_instance.propagate = enable
        super().__setitem__(name, logger_instance)


def whitelist_logging():
    logging.root.manager.loggerDict = WhitelistLoggerDict(
        logging.root.manager.loggerDict.copy()
    )


def blacklist_logging():
    for logger_name in _logger_blacklist:
        logging.getLogger(logger_name).setLevel(logging.FATAL)


def configure_logging():
    global _logger
    _logger.remove(0)
    _logger.add(
        sys.stdout,
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format=_logger_format,
        backtrace=False,
        filter=filter_logs,
    )
    _logger = _logger.patch(hide_secrets)

    whitelist_logging()
    blacklist_logging()

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)

    # configure default logging
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
