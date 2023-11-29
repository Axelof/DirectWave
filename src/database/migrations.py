import contextlib

from aerich import Command
from loguru import logger

from database.config import config
from settings import settings

MIGRATIONS_DIR = settings.PROJECT_DIR.joinpath('migrations')


async def run_migration():
    command = Command(tortoise_config=config, location=MIGRATIONS_DIR)
    logger.info('Run database migration...')
    await command.init()
    with contextlib.suppress(FileExistsError):
        await command.init_db(safe=True)
    # noinspection PyBroadException
    try:
        await command.migrate()
        await command.upgrade()  # noqa
        logger.info('Database successfully upgraded')
    except BaseException:
        logger.error('Database failed to upgrade')
