from ZapMail.emailer import Emailer

# Replace with your actual Gmail address and app password
emailer = Emailer(
    sender_email="testingmessagebot@gmail.com",
    password="wlpcnhebeiqdafqg"
)

# Send a real email
success = emailer.send_email(
    recipient="gd.familie.18@gmail.com",
    subject="Hello from ZapMail!",
    body_text="This is a real email sent using ZapMail.",
    body_html="<h1>This is a real email sent using <b>ZapMail</b>.</h1>"
)

if success:
    print("Email sent successfully!")
else:
    print("Failed to send email.")