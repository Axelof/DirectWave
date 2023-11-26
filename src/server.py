import gettext
import logging

from fastapi import FastAPI
from fastapi.routing import APIRoute

from definitions import LOCALES_DOMAIN, LOCALES_DIR
from scheduler import scheduler
from settings import settings

from routes import routers
import middlewares  # noqa


gettext.install(LOCALES_DOMAIN, LOCALES_DIR)


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}" if len(route.tags) else f"unmarked-{route.name}"


app = FastAPI(
    generate_unique_id_function=custom_generate_unique_id,
    on_startup=[
        scheduler.start
    ],
    on_shutdown=[
        scheduler.shutdown
    ]
)


for router in routers:
    app.include_router(router.router)


if settings.DOMAIN:
    logging.info(f'https://{settings.DOMAIN}')