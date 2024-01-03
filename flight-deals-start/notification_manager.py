import os
from twilio.rest import Client

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.sid = os.environ.get("TWILIO_SID")
        self.auth_token = os.environ.get("TWI_AUTH_TOKEN")
        self.some_num = os.environ.get("SOME_NUM")

    def send_text(self, msg):
        client = Client(self.sid, self.auth_token)
        status = client.messages.create(to="+16362845670", from_=self.some_num, body=msg)
        return status