import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import os
from ai_news_config import SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_LIST
def send_email(report_path):
    # Get the date of the day before the email is sent out
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Email configuration
    sender_email = SENDER_EMAIL
    sender_password = SENDER_PASSWORD
    subject = f"Automated AI Report - {today}"
    body = f"Automated AI Report for {today}."
    
    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["Subject"] = subject
    
    # Set the "To" header with all the recipients
    recipient_list = RECIPIENT_LIST
    message["To"] = ", ".join(recipient_list)
    
    message.attach(MIMEText(body, "plain"))
    
    # Attach the .docx file
    with open(report_path, "rb") as attachment:
        part = MIMEApplication(attachment.read(), _subtype="octet-stream")
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(report_path)}")
        message.attach(part)
    
    # Connect to the Gmail SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    
    # Send the email
    server.send_message(message)
    
    # Disconnect from the SMTP server
    server.quit()
    
    print("Email sent successfully.")
