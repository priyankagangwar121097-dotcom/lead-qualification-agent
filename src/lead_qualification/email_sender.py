import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


def send_email(sender_email, sender_password, receiver_email, subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()

        print(f"EMAIL SENT SUCCESSFULLY to {receiver_email}")
        return True

    except Exception as e:
        print(f"EMAIL FAILED for {receiver_email}: {e}")
        return False


def route_email(lead_status, lead_name, lead_email):

    lead_status = lead_status.upper().strip()

    if lead_status == "HOT":
        sender_email = os.getenv("GHC_EMAIL")
        sender_password = os.getenv("GHC_EMAIL_PASSWORD")

        subject = "Quick discussion"

        body = f"""Hi {lead_name},

Thank you for your interest.

I would love to connect with you for a quick discussion to understand your requirements better.

Please let me know a convenient time to connect.

Best regards,
Priyanka
"""

        return send_email(
            sender_email,
            sender_password,
            lead_email,
            subject,
            body
        )

    elif lead_status == "WARM":
        sender_email = os.getenv("GMAIL_EMAIL")
        sender_password = os.getenv("GMAIL_APP_PASSWORD")

        subject = "Let's connect"

        body = f"""Hi {lead_name},

Thank you for your interest.

I wanted to connect and understand your requirements better.

Please let me know if you would be available for a quick discussion.

Best regards,
Priyanka
"""

        return send_email(
            sender_email,
            sender_password,
            lead_email,
            subject,
            body
        )

    elif lead_status == "COLD":
        print(f"NO EMAIL SENT: {lead_name} is a COLD lead.")
        return False

    else:
        print(f"UNKNOWN LEAD STATUS: {lead_status}")
        return False