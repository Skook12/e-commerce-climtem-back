import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.model import User


def sendEmail(u: User, html_body: str, config):    
    message = MIMEMultipart()
    message['From'] = config['email']
    message['To'] = u.email
    message['Subject'] = "Confirme a criação da sua conta na Climtem"

    message.attach(MIMEText(html_body, 'html'))
    smtp_server = "smtp.gmail.com"
    port = 587
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(config['email'], config['p'])
        server.sendmail(config['email'], u.email, message.as_string())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()