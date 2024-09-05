# email_utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    smtp_server = 'localhost'
    smtp_port = 1025

    from_email = 'your-email@example.com'
 
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = "ghjk@vb"
    msg['Subject'] = "subject"

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.sendmail(from_email, to_email, msg.as_string())
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')
