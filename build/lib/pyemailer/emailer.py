import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class Emailer:
    def __init__(self, sender_email, password, smtp_server="smtp.gmail.com", smtp_port=465, silent=False):
        self.sender_email = sender_email
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.silent = silent

    def send_email(self, recipient, subject, body_text, body_html=None, attachments=None, cc=None, bcc=None):
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = recipient
        msg["Subject"] = subject
        if cc:
            msg["Cc"] = cc
        if bcc:
            msg["Bcc"] = bcc
        msg.attach(MIMEText(body_text, "plain"))
        if body_html:
            msg.attach(MIMEText(body_html, "html"))
        for filepath in attachments or []:
            part = MIMEBase("application", "octet-stream")
            with open(filepath, "rb") as f:
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={filepath}")
            msg.attach(part)

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.sender_email, self.password)
                server.send_message(msg)
            if not self.silent:
                print(f"Email successfully sent to {recipient}")
        except Exception as e:
            print(f"Failed to send email to {recipient}: {e}")
