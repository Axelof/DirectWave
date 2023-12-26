import gettext

from fastapi import FastAPI
from fastapi.routing import APIRoute
from loguru import logger

from definitions import LOCALES_DOMAIN, LOCALES_DIR
from scheduler import scheduler
from settings import settings

from routes import routers
import middlewares  # noqa
from logger import configure_logging
import mail.signals


gettext.install(LOCALES_DOMAIN, LOCALES_DIR)
configure_logging()


def custom_generate_unique_id(route: APIRoute):
    return (
        f"{route.tags[0]}-{route.name}" if len(route.tags) else f"unmarked-{route.name}"
    )


app = FastAPI(
    generate_unique_id_function=custom_generate_unique_id,
    on_startup=[scheduler.start, mail.signals.on_startup],
    on_shutdown=[scheduler.shutdown, mail.signals.on_shutdown],
)


for router in routers:
    app.include_router(router.router)


if settings.DOMAIN:
    logger.info(f"https://{settings.DOMAIN}")
