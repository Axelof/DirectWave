from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP
from jinja2 import Environment, FileSystemLoader
from loguru import logger

from settings import settings
from definitions import FILES_DIR


class SMTPModule:
    def __init__(self):
        self.host = settings.EMAIL_HOST
        self.port = settings.EMAIL_PORT
        self.user = settings.EMAIL_USER
        self.password = settings.EMAIL_PASSWORD

        self._jinja = Environment(loader=FileSystemLoader(FILES_DIR))
        self._server = SMTP(hostname=self.host, port=self.port, use_tls=True)

        self.template = self._jinja.get_template("mail/template.html")

    async def start(self):
        await self._server.connect()
        await self._server.login(self.user, self.password)
        logger.debug(f"SMTP connected: {self.host}:{self.port} ({self.user})")

    async def shutdown(self):
        await self._server.quit()
        logger.debug("SMTP connection closed")

    async def verify(self, receiver: str):
        message = MIMEMultipart("alternative")

        message["Subject"] = "DirectWave Verify"
        message["From"] = self.user
        message["To"] = receiver

        message.attach(
            MIMEText(
                self.template.render(
                    date=datetime.now().strftime("%d.%m.%Y (%H:%M)"),
                    verify_endpoint="https://google.com/",  # TODO: replace
                    incorrect_endpoint="https://google.com/",  # TODO: replace
                ),
                "html",
            )
        )

        await self._server.send_message(message)


mail = SMTPModule()
