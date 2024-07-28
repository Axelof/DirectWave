from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Self

from aiosmtplib import SMTP
from jinja2 import Environment, FileSystemLoader

from settings import settings
from definitions import FILES_DIR


class SMTPModule:
    def __init__(self):
        self.host = settings.mail.host
        self.port = settings.mail.port
        self.username = settings.mail.username
        self.password = settings.mail.password

        self._jinja = Environment(loader=FileSystemLoader(FILES_DIR))
        self._server = SMTP(hostname=self.host, port=self.port, use_tls=True)

        self.template = self._jinja.get_template("mail/template.html")

    async def start(self) -> Self:
        await self._server.connect()
        await self._server.login(self.username, self.password)

        return self

    async def shutdown(self) -> None:
        await self._server.quit()

    async def verify(self, receiver: str):
        message = MIMEMultipart("alternative")

        message["Subject"] = "DirectWave Verify"
        message["From"] = self.username
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
