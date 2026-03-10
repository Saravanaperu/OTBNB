import aiosmtplib
from email.message import EmailMessage
import structlog

from backend.config.settings import settings
from backend.alerts.email_templates import get_template

logger = structlog.get_logger()


class EmailService:
    def __init__(self):
        self.hostname = "smtp.gmail.com"
        self.port = 465
        self.username = settings.gmail_user
        self.password = settings.gmail_app_pass
        self.recipient = settings.alert_email

    async def send_email(self, subject: str, html_content: str) -> bool:
        if self.username == "dummy@gmail.com":
            logger.warning(
                "Email service not configured. Skipping email send.", subject=subject
            )
            return False

        message = EmailMessage()
        message["From"] = self.username
        message["To"] = self.recipient
        message["Subject"] = subject
        message.set_content(html_content, subtype="html")

        try:
            await aiosmtplib.send(
                message,
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=True,
            )
            logger.info("Email sent successfully", subject=subject)
            return True
        except Exception as e:
            logger.error("Failed to send email", error=str(e), subject=subject)
            return False

    async def send_trade_alert(self, trade_data: dict):
        subject = f"Trade Alert: {trade_data.get('action')} {trade_data.get('symbol')}"
        html_content = get_template("trade_alert").render(trade=trade_data)
        return await self.send_email(subject, html_content)

    async def send_error_alert(self, error_msg: str):
        subject = "Bot Error Alert"
        html_content = get_template("error_alert").render(error_msg=error_msg)
        return await self.send_email(subject, html_content)
