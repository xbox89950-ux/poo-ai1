"""Email sending utility"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

logger = logging.getLogger(__name__)

class EmailSender:
    SMTP_SERVERS = {
        "gmail": ("smtp.gmail.com", 587),
        "outlook": ("smtp.office365.com", 587),
        "yahoo": ("smtp.mail.yahoo.com", 587),
    }

    @staticmethod
    def send_email(to: str, subject: str, body: str, from_email: str = None, password: str = None, provider: str = "gmail") -> str:
        if not from_email or not password:
            return "Please provide sender email and password."
        try:
            host, port = EmailSender.SMTP_SERVERS.get(provider, ("smtp.gmail.com", 587))
            msg = MIMEMultipart()
            msg["From"] = from_email
            msg["To"] = to
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP(host, port)
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            server.quit()
            return f"Email sent to {to}"
        except Exception as e:
            return f"Email error: {e}"
