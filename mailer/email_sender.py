import os
import smtplib
from email.mime.text import MIMEText


# =========================================================
# EMAIL SENDER
# Sends final HTML digest
# =========================================================

def send_email(html_body, subject):

    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    EMAIL_TO = os.getenv("EMAIL_TO")

    msg = MIMEText(html_body, "html")
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    print("\n📧 Sending email...\n")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(msg)
    server.quit()

    print("Email sent successfully ✅\n")
