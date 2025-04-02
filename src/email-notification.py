import json
import random
import smtplib, ssl
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SendMail:
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"


    subject = "[[EDK][Pruszków][2024][św Kazimierz]"
    def __init__(self):
            with open('email-phases.json', 'r', encoding="utf8") as file:
                self.content = json.load(file)  # Odczyt całej zawartości pliku

    def create_message(self):
        message = MIMEMultipart()
        message['Subject'] = self.subject
        message['From'] = self.sender_email
        message['To'] = self.recipient_email

        greeting = Szczęść Boże
        status_message, number_of_tests, passes, failures = self.get_tests_stats()

        html_content = """
        <html>
          <body>
            <div style="color:black;">""" + greeting + """</div>
            <div><br></div>
            <div style="color:black;">""" + intro + """</div>
            <div><br></div>
            <div style="color:black;"><b>LINK DO RAPORTU: https://risk-e2e-tests-80b2c3.gitlab.io/mochawesome-report/report.html</b></div>
            """ + status_message + """
            <div style="color:blue;"><b>ILOŚĆ TESTÓW: """ + str(number_of_tests) + """</b></div>
            <div style="color:green;"><b>PRZESZŁY: """ + str(passes) + """</b></div>
            <div style="color:red;"><b>PORAŻKI: """ + str(failures) + """</b></div>
            <div><br></div>
            <div style="color:black;">""" + signature + """</div>
          </body>
        </html>
        """
        message.attach(MIMEText(html_content, 'html'))
        return message

    def send_mail(self):
        message = self.create_message()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.recipient_email, message.as_string())


SendMail().send_mail()
