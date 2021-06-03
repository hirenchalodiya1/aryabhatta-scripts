import smtplib
from email.mime.text import MIMEText
from datetime import datetime as dt
from decouple import config


def send_mail(subject, text):
    print("[ " + dt.strftime(dt.now(), "%d-%m-%Y %H:%M:%S") + " ] Sending Mail...")
    smtp_ssl_host = config("HOST", cast=str)  # smtp.mail.yahoo.com
    smtp_ssl_port = config("PORT", cast=int)
    username = config("SMTP_USERNAME", cast=str)
    password = config("PASSWORD", cast=str)
    sender = config("SENDER", cast=str)
    targets = config("RECEIVER", cast=lambda v: [x.strip() for x in v.split(',')])

    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(targets)

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(sender, targets, msg.as_string())
    server.quit()

    print("[ " + dt.strftime(dt.now(), "%d-%m-%Y %H:%M:%S") + " ] Mail Sent")
