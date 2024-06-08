import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configs.config import Config

def sendEmail(email: str, html_body: str, subject: str):    
    message = MIMEMultipart()
    message['From'] = Config.STMP_SETTINGS['email']
    message['To'] = email
    message['Subject'] = subject

    message.attach(MIMEText(html_body, 'html'))
    smtp_server = "smtp.gmail.com"
    port = 587
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(Config.STMP_SETTINGS['email'], Config.STMP_SETTINGS['p'])
        server.sendmail(Config.STMP_SETTINGS['email'], email, message.as_string())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()