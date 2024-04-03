import os
from security import safe_requests
import requests

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.project = "myFlightDeals"
        self.flight_sheet = "sheet1"
        self.user_sheet = "sheet2"
        self.auth = os.environ.get("SHEETY_AUTH")

        self.header = {
            'Authorization': self.auth
        }

        self.flight_sheet_endpoint = (f"https://api.sheety.co/bfcaa73edd17edb613cd16a2c54f110c/{self.project}/{self.flight_sheet}")

        self.user_sheet_endpoint = (f"https://api.sheety.co/bfcaa73edd17edb613cd16a2c54f110c/{self.project}/{self.user_sheet}")
        self.city = "city"
        self.iata_code = "iataCode"
        self.lowest_price = "lowestPrice"
        self.departure = "departureDate"

    def api_get( self, my_endpoint):
        sheet_data = safe_requests.get(url=my_endpoint, headers=self.header)
        sheet_data.raise_for_status()
        return sheet_data

    def api_post(self, my_endpoint, sheety_parameters):
        s_response = requests.post(url=my_endpoint, json=sheety_parameters, headers=self.header)
        s_response.raise_for_status()
        return s_response
