import aiosmtplib
from email.message import EmailMessage
from constant.index import SMTP_PASSWORD, SMTP_PORT, SMTP_SERVER, SMTP_USERNAME


async def send_email_alert(subject: str, body: str, to_email: str):
    msg = EmailMessage()
    msg["From"] = SMTP_USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        await aiosmtplib.send(
            msg,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
        )
        print("✅ Email alert sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        