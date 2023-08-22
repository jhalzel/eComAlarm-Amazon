import email, smtplib, ssl
from providers import PROVIDERS
import os

from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from os.path import basename

from exceptions import (
    ProviderNotFoundException,
    NoMMSSupportException,
    NumberNotValidException,
)

import json

# Read the threshold value from the config.json file
with open('config.json', 'r') as file:
    config = json.load(file)
    threshold = int(config.get('fbm_threshold', 0))  # Default to 0 if not found
    

gmail_credentials = {
    "gmail_username": os.environ.get("GMAIL_USER"),
    "gmail_password": os.environ.get("GMAIL_PASSWORD"),
}

def send_sms_via_email(
    number: str,
    message: str,
    provider: str,
    sender_credentials: tuple,
    subject: str = '',
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):
    
    # number = validate_number(number)
    sender_email, email_password = sender_credentials
    receiver_email = f"{number}@{PROVIDERS.get(provider).get('sms')}"

    # email_message = f"Subject: {subject}\nTo:{receiver_email}\n{message}"

    # with smtplib.SMTP_SSL(
    #     smtp_server, smtp_port, context=ssl.create_default_context()
    # ) as email:
    #     email.login(sender_email, email_password)
    #     email.sendmail(sender_email, receiver_email, email_message)

    message = 'https://apps.apple.com/us/app/amazon-seller/id794141485'

     # Create a MIMEText object with HTML content
    html_content = f'<html><body><p>Total sales has met the threshold of ${threshold}. Check Amazon Seller Central: </>{message}</body></html>'
    email_message = MIMEMultipart("alternative")
    email_message.attach(MIMEText(html_content, "html"))

    email_message["Subject"] = subject
    email_message["From"] = sender_email
    email_message["To"] = receiver_email

     # Explicitly create an anchor tag with the href attribute
    anchor_tag = f' <a href="{message}"></a>'
    message_with_link = f'Visit Amazon Seller{anchor_tag}'

    email_message.attach(MIMEText(message_with_link, "html"))

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message.as_string())




