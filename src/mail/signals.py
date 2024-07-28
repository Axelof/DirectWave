from mail import mail


async def sp_():
    smtp = await mail.start()

    return f"SMTP connected ({smtp.host}:{smtp.port} - {smtp.username})"


async def sn_():
    await mail.shutdown()

    return "SMTP connection closed"
