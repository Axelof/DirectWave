from loguru import logger

from mail import mail


async def on_startup():
    await mail.start()
    from JWT import JWT
    logger.info(JWT.sign(20, []))


async def on_shutdown():
    await mail.shutdown()
