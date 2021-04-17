import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import config



def SendEmail(buy, sell):
    mail_content = F'''Ola ,
        Abaixo segue a relação de criptomoedas, com a recomendação do Trading View

        Forte venda: {sell}

        Forte Compra: {buy}
        '''
    now = datetime.now()

    sender_address = config.GMAIL_EMAIL
    sender_pass = config.GMAIL_PASSWORD
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

    sender_address = config.GMAIL_EMAIL
    sender_pass = config.GMAIL_PASSWORD
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

    sender_address = config.GMAIL_EMAIL
    sender_pass = config.GMAIL_PASSWORD
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
    
    
def SendEmailBuy(price, buy):
    mail_content = F'''Compra efetuada com sucesso !!! ,
        Valor comprado: {price}
        
        Order ID: {buy.get('orderId')}
        Data {data}
        '''
    now = datetime.now()

    sender_address = config.GMAIL_EMAIL
    sender_pass = config.GMAIL_PASSWORD
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
    
    
def SendEmailSell(price, sell):
    mail_content = F'''Venda efetuada com sucesso !!! ,
        Valor Vendido: {price}
        
        Sell: {sell}
        '''
    now = datetime.now()

    sender_address = config.GMAIL_EMAIL
    sender_pass = config.GMAIL_PASSWORD
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