from mail import mail


async def on_startup():
    await mail.start()


async def on_shutdown():
    await mail.shutdown()
