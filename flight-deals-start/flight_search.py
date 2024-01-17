import os
import requests
from security import safe_requests
from datetime import datetime
from data_manager import DataManager

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        now = datetime.now()
        tomorrow = datetime.now().day + 1
        self.date_start_range = datetime(year=now.year, month=now.month, day=tomorrow).strftime("%d/%m/%Y")
        self.date_end_range = datetime(year=now.year, month=(now.month + 6), day=tomorrow).strftime("%d/%m/%Y")

        self.endpoint = "https://api.tequila.kiwi.com/v2/search"
        self.loc_que_ext = "/locations/query"

        self.header = {
            "apikey": os.environ.get("TEQ_API_KEY")
        }

    def get_post_parameters(self, my_destination):
        parameters = {
            "fly_from": "STL",
                "fly_to": my_destination,
                "date_from": self.date_start_range,
                "date_to": self.date_end_range,
                "curr": "USD"
        }
        return parameters

    def api_call(self, t_parameters):
        teq_response = safe_requests.get(url=self.endpoint, params=t_parameters, headers=self.header)
        teq_response.raise_for_status()
        return teq_response

    def get_iata_codes(self, s_data):
        loc_query_endpoint = self.endpoint.replace("/v2/search", self.loc_que_ext)
        i = 0
        for entry in s_data['sheet1']:
            destination = {
                "term": entry['city']
            }
            location_query = safe_requests.get(url=loc_query_endpoint, params=destination, headers=self.header)
            location_query.raise_for_status()
            loc_que_json = location_query.json()
            s_data["sheet1"][i]['iataCode'] = loc_que_json['locations'][0]['code']
            if s_data["sheet1"][i]["city"] == 'Bali':
                s_data["sheet1"][i]["iataCode"] = "DPS"
            new_parameters = {
                "sheet1": {
                    "city": s_data["sheet1"][i]["city"],
                    "iataCode": s_data["sheet1"][i]["iataCode"],
                    "lowestPrice": s_data["sheet1"][i]["lowestPrice"]
                }
            }
            sheety = DataManager()
            put_endpoint = f"{sheety.flight_sheet_endpoint}/{s_data['sheet1'][i]['id']}"
            status = requests.put(url=put_endpoint, json=new_parameters, headers=sheety.header)
            status.raise_for_status()
            i += 1
