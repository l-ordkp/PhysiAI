import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv()

def send_email(state):
    # Create the email message
    
    msg = MIMEMultipart()
    msg['From'] = os.getenv("EMAIL")
    msg['To'] = state['recipient_email']
    msg['Subject'] = state['subject']

    # Attach the email body
    msg.attach(MIMEText(state['body'], 'plain'))

    try:
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(os.getenv("EMAIL"), os.getenv("APP_PASSWORD"))
        server.sendmail(os.getenv("EMAIL"), state['recipient_email'], msg.as_string())
        server.quit()
        state['result'] = "Email sent successfully"
        return state
    except Exception as e:
        state['result'] = f"Failed to send email: {str(e)}"
        return state
    



