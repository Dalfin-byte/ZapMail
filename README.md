# ZapMail

`ZapMail` is a simple Python library to send emails via Gmail's SMTP server. It supports plain text, HTML content, attachments, and CC/BCC fields.

## Installation

```bash
pip install ZapMail
```


```python
from ZapMail.emailer import Emailer

emailer = Emailer(
    sender_email="your_email@gmail.com",
    password="your_app_password"
)

success = emailer.send_email(
    recipient=["recipient1@example.com", "recipient2@example.com"],
    subject="ZapMail Feature Demo",
    body_text="This is a plain text body.",
    body_html="""
        <h1>ZapMail Demo</h1>
        <p>This email demonstrates <b>ZapMail</b> features.</p>
        <img src="cid:demoimg">
    """,
    attachments=["/path/to/attachment.pdf"],
    cc="ccperson@example.com",
    bcc=["bcc1@example.com", "bcc2@example.com"],
    reply_to="replyto@example.com",
    inline_images={"demoimg": "/path/to/image.png"},
    custom_headers={"X-Custom-Header": "ZapMailDemo"}
)

if success:
    print("Email sent successfully!")
else:
    print("Failed to send email.")

```