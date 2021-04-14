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
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = F'BOT - CRIPTOMOEDAS - {now}' 
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')