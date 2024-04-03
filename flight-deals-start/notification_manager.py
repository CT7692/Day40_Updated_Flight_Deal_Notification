import os
import smtplib


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.my_email = "jrydel92@gmail.com"
        self.pw = os.environ.get("GMAIL_PW")

    def send_email(self, msg, email):
        message = f"Subject: Low price alert!\n\n{msg}".encode('utf-8')
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.my_email, password=self.pw)
            connection.sendmail(from_addr=self.my_email, to_addrs=email,
                                msg=message)
