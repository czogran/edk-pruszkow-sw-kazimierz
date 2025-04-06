from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import smtplib, ssl

subject = "[EDK][Pruszków][2024][św Kazimierz]"
year=2025

port = 587  # For starttls
smtp_server = "smtp.gmail.com"


with open('test.json', 'r', encoding="utf8") as file:
        file_content = json.load(file)  
        password =file_content.get('password')
        sender_email = file_content.get('senderEmail')

with open('mails.txt', 'r', encoding="utf8") as file:
        receiver_emails = []
        for line in file:
              receiver_emails.append(line.rstrip('\n'))


with open("../"+year+'/email-content.html', 'r', encoding="utf8") as file:
        html_content = file.read()  

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    for receiver_email in receiver_emails:
        print("send to: " + receiver_email)
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = receiver_email

        message.attach(MIMEText(html_content, 'html'))
        message = message.as_string()
        server.sendmail(sender_email, receiver_email, message)
