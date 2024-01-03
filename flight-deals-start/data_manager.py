import os
from security import safe_requests

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.project = "myFlightDeals"
        self.sheet = "sheet1"
        self.auth = os.environ.get("SHEETY_AUTH")

        self.header = {
            "Authorization" : self.auth
        }

        self.endpoint = f"https://api.sheety.co/bfcaa73edd17edb613cd16a2c54f110c/{self.project}/{self.sheet}"
        self.city = "city"
        self.iata_code = "iataCode"
        self.lowest_price = "lowestPrice"
        self.departure = "departureDate"

    def get_parameters(self, data, my_dict):
        parameters = {
           self.sheet: {
               "city": data["data"][0]["cityTo"],
               "iataCode": data["data"][0]["flyTo"],
               "lowestPrice": my_dict["price"],
               "departureDate": my_dict["departure"]
           }
        }
        return parameters