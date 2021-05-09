
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv
from helpers import *

dotenv_path = join(dirname(__file__), '.env')
local_env = load_dotenv(dotenv_path)


if local_env:
    GMAIL_EMAIL = os.environ.get("GMAIL_EMAIL")
    GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")
    GMAIL_RECEIVER_ADDRES = os.environ.get("GMAIL_RECEIVER_ADDRES")
else:
    GMAIL_EMAIL = os.environ.get("GMAIL_EMAIL")
    GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")
    GMAIL_RECEIVER_ADDRES = os.environ.get("GMAIL_RECEIVER_ADDRES")


class Gmail(object):
    def __init__(self, email, password):
        self.email = GMAIL_EMAIL
        self.password = GMAIL_PASSWORD
        self.server = 'smtp.gmail.com'
        self.port = 587
        session = smtplib.SMTP(self.server, self.port)        
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(self.email, self.password)
        self.session = session

    def send_email(self, subject, body):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = GMAIL_RECEIVER_ADDRES
        msg['MIME-Version'] = '1.0'
        msg['Content-Type'] = 'text/html'
        body_send = MIMEText(body, 'html')
        msg.attach(body_send)
        self.session.sendmail(
            self.email,
            GMAIL_RECEIVER_ADDRES,
            msg.as_string())
