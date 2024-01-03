import os
from security import safe_requests
from datetime import datetime

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        now = datetime.now()
        tomorrow = datetime.now().day + 1
        self.flight_date = datetime(year=now.year, month=now.month, day=tomorrow).strftime("%d/%m/%Y")
        self.return_date = datetime(year=now.year, month=(now.month + 6), day=tomorrow).strftime("%d/%m/%Y")

        self.endpoint = "https://api.tequila.kiwi.com/v2/search"

        self.header = {
            "apikey": os.environ.get("TEQ_API_KEY")
        }

    def get_parameters(self, my_destination):
        parameters = {
            "fly_from": "STL",
            "fly_to": my_destination,
            "date_from": self.flight_date,
            "date_to": self.return_date,
            "curr": "USD"
        }
        return parameters