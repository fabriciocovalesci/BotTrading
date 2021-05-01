import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
local_env = load_dotenv(dotenv_path)


if local_env:
    GMAIL_EMAIL = os.environ.get("GMAIL_EMAIL")
    GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")
else:
    GMAIL_EMAIL = os.environ.get("GMAIL_EMAIL")
    GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")


def SendEmail(buy, sell):
    mail_content = F'''Ola ,
        Abaixo segue a relação de criptomoedas, com a recomendação do Trading View

        Forte venda: {sell}

        Forte Compra: {buy}
        '''
    now = datetime.now()

    sender_address = GMAIL_EMAIL
    sender_pass = GMAIL_PASSWORD
    receiver_address = 'fabcovalesci@gmail.com'

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = F'BOT - CRIPTOMOEDAS - {now.strftime("%d-%m-%y %H:%M:%S")}' 
 
    message.attach(MIMEText(mail_content, 'plain'))
 
    session = smtplib.SMTP('smtp.gmail.com', 587) 
    session.starttls()
    session.login(sender_address, sender_pass) 
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


def SendEmailDeploy():
    mail_content = F'''Ola ,
        Deploy executado com sucesso !!
        '''
    now = datetime.now()

    sender_address = GMAIL_EMAIL
    sender_pass = GMAIL_PASSWORD
    receiver_address = 'fabcovalesci@gmail.com'
    
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = F'BOT - CRIPTOMOEDAS - {now.strftime("%d-%m-%y %H:%M:%S")}' 

    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587) 
    session.starttls() 
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
    
    
def SendEmailERROR(error, data):
    mail_content = F'''Ola ,
        Ocorrido um erro {error} !!
        
        Data {data}
        '''
    now = datetime.now()

    sender_address = GMAIL_EMAIL
    sender_pass = GMAIL_PASSWORD
    receiver_address = 'fabcovalesci@gmail.com'
    
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = F'BOT - CRIPTOMOEDAS - {now.strftime("%d-%m-%y %H:%M:%S")}' 

    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587) 
    session.starttls() 
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
    
    
def SendEmailBuy(priceBuy, date):
    mail_content = f'''Compra efetuada com sucesso !!! ,
        
        Valor comprado: {priceBuy}
        Data: {date}
        
        '''
    now = datetime.now()

    sender_address = GMAIL_EMAIL
    sender_pass = GMAIL_PASSWORD
    receiver_address = 'fabcovalesci@gmail.com'
    
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = F'BOT - CRIPTOMOEDAS - {now.strftime("%d-%m-%y %H:%M:%S")}' 

    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587) 
    session.starttls() 
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
    
    
def SendEmailSell(orderSell, date):
    mail_content = f'''Venda efetuada com sucesso !!! ,
        
        Order Venda: {orderSell}
        Data: {date}
        '''
    now = datetime.now()

    sender_address = GMAIL_EMAIL
    sender_pass = GMAIL_PASSWORD
    receiver_address = 'fabcovalesci@gmail.com'
    
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = f'BOT - CRIPTOMOEDAS - {now.strftime("%d-%m-%y %H:%M:%S")}' 

    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587) 
    session.starttls() 
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')