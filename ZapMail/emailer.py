"""
ZapMail/emailer.py

A simple, intuitive Gmail SMTP email library supporting plain text, HTML, attachments, CC/BCC, inline images, and custom headers.
"""

import smtplib
import ssl
import os
import logging
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate, make_msgid
from typing import Union, List, Dict


class Emailer:
    def __init__(
        self,
        sender_email: str,
        password: str,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 465,
        silent: bool = False,
        logger: logging.Logger = None
    ):
        """
        Initialize Emailer.
        :param sender_email: your email address
        :param password: your SMTP password (e.g., Gmail app password)
        :param smtp_server: SMTP server address
        :param smtp_port: SMTP SSL port (default: 465)
        :param silent: if True, suppresses success messages
        :param logger: optional logger instance
        """
        self.sender_email = sender_email
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.silent = silent
        self.logger = logger or logging.getLogger(__name__)

    def send_email(
        self,
        recipient: Union[str, List[str]],
        subject: str,
        body_text: str,
        body_html: str = None,
        attachments: List[str] = None,
        cc: Union[str, List[str]] = None,
        bcc: Union[str, List[str]] = None,
        reply_to: str = None,
        inline_images: Dict[str, str] = None,  # cid: filepath
        custom_headers: Dict[str, str] = None
    ) -> bool:
        """
        Send an email.
        :param recipient: str or list of recipients
        :param subject: subject of the email
        :param body_text: plain-text body
        :param body_html: optional HTML body
        :param attachments: list of file paths to attach
        :param cc: str or list of CC recipients
        :param bcc: str or list of BCC recipients
        :param reply_to: optional reply-to email address
        :param inline_images: dictionary of inline images (cid: filepath)
        :param custom_headers: dictionary of custom email headers
        :return: True if email was sent successfully, False otherwise
        """
        # Normalize recipients and flatten lists
        def normalize(val):
            if not val:
                return []
            if isinstance(val, str):
                items = [v.strip() for v in val.split(",") if v.strip()]
                return items
            result = []
            for v in val:
                result += [email.strip() for email in v.split(",") if email.strip()]
            return result

        recipient_list = normalize(recipient)
        cc_list = normalize(cc)
        bcc_list = normalize(bcc)

        msg = MIMEMultipart("related")
        msg["From"] = self.sender_email
        msg["To"] = ", ".join(recipient_list)
        msg["Subject"] = subject
        if cc_list:
            msg["Cc"] = ", ".join(cc_list)
        if reply_to:
            msg["Reply-To"] = reply_to
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid()
        if custom_headers:
            for k, v in custom_headers.items():
                msg[k] = v

        # Attach message bodies
        alt = MIMEMultipart("alternative")
        alt.attach(MIMEText(body_text, "plain"))
        if body_html:
            alt.attach(MIMEText(body_html, "html"))
        msg.attach(alt)

        # Attach files with correct MIME type
        for filepath in attachments or []:
            try:
                mime_type, _ = mimetypes.guess_type(filepath)
                main_type, sub_type = ("application", "octet-stream")
                if mime_type:
                    parts = mime_type.split("/")
                    if len(parts) == 2:
                        main_type, sub_type = parts
                part = MIMEBase(main_type, sub_type)
                with open(filepath, "rb") as f:
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                filename = os.path.basename(filepath)
                part.add_header("Content-Disposition", f"attachment; filename={filename}")
                msg.attach(part)
            except Exception as e:
                self.logger.error(f"Attachment error: {filepath}: {e}")

        # Attach inline images with correct MIME type
        for cid, img_path in (inline_images or {}).items():
            try:
                mime_type, _ = mimetypes.guess_type(img_path)
                main_type, sub_type = ("image", "png")
                if mime_type:
                    parts = mime_type.split("/")
                    if len(parts) == 2:
                        main_type, sub_type = parts
                with open(img_path, "rb") as img:
                    img_part = MIMEBase(main_type, sub_type)
                    img_part.set_payload(img.read())
                encoders.encode_base64(img_part)
                img_part.add_header("Content-ID", f"<{cid}>")
                img_part.add_header("Content-Disposition", "inline")
                msg.attach(img_part)
            except Exception as e:
                self.logger.error(f"Inline image error: {img_path}: {e}")

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.sender_email, self.password)
                all_recipients = recipient_list + cc_list + bcc_list
                server.send_message(msg, from_addr=self.sender_email, to_addrs=all_recipients)
            if not self.silent:
                print(f"✅ Email successfully sent to: {msg['To']}")
            return True
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            self.logger.error(f"Failed to send email: {e}")
            return False
