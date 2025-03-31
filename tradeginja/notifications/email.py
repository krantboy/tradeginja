import smtplib
from email.mime.text import MIMEText
from .base import Notifier

class EmailNotifier(Notifier):
    """Email-specific notifier."""
    def __init__(self, sender_email: str, receiver_email: str, password: str,
                 smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def notify(self, subject: str, body: str):
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(msg)
            print(f"Email sent to {self.receiver_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")