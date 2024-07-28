from fastapi import FastAPI
from fastapi.routing import APIRoute
from loguru import logger

from scheduler import scheduler
from settings import settings

from routes import routers
import middlewares  # noqa
from signals import WatchSignals
from utils.logger import configure_logging
from utils.i18n import configure_gettext
import mail.signals


configure_gettext()
configure_logging()

signals_watcher = WatchSignals()

app = FastAPI(
    on_startup=[signals_watcher.on_startup, scheduler.start],
    on_shutdown=[signals_watcher.on_shutdown, scheduler.shutdown],
)


for router in routers:
    app.include_router(router.router)


if settings.project.domain:
    logger.info(f"https://{settings.project.domain}")
