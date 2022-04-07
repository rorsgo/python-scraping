import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(body):
    try:
        email = list(os.getenv("EMAIL_RECIPIENTS").split(","))
        for recipient in email:
            message = MIMEMultipart()
            message['From'] = os.getenv("EMAIL_SENDER")
            message['To'] = recipient
            message['Subject'] = "UDI available appointments"
            message.attach(MIMEText(body, 'plain'))
            session = smtplib.SMTP(os.getenv("EMAIL_HOST"), os.getenv("EMAIL_PORT"))
            session.starttls()
            session.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
            session.sendmail(os.getenv("EMAIL_SENDER"), recipient, message.as_string())
            session.quit()
        print("Email sent successfully.")
        exit(0)
    except Exception as e:
        print(e)