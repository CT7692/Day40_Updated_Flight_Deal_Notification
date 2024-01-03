#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from flight_data import FlightData
from security import safe_requests
import requests

TRAVEL_DICT = {
    "Giza": "SPX",
    "Paris": "PAR",
    "Rome": "ROM",
    "Sao Paulo": "SAO",
    "Tokyo": "TYO"
}

def tequila_api_call():
    t_response = safe_requests.get(url=tequila.endpoint, params=teq_parameters, headers=tequila.header)
    t_response.raise_for_status()
    t_json = t_response.json()
    return t_json

def sheety_api_call():
    s_response = requests.post(url=sheety.endpoint, json=sheety_parameters, headers=sheety.header)
    s_response.raise_for_status()
    return s_response

def format_message():
    my_message = (f'Low price alert! Only ${sheety_parameters[sheety.sheet][sheety.lowest_price]}'
               f' to fly from Saint Louis-STL to {sheety_parameters[sheety.sheet][sheety.city]}-'
               f'{sheety_parameters[sheety.sheet][sheety.iata_code]} on {sheety_parameters[sheety.sheet][sheety.departure]}.')
    return  my_message

tequila = FlightSearch()
sheety = DataManager()
twi = NotificationManager()

teq_parameters = tequila.get_parameters(TRAVEL_DICT["Paris"])
teq_json = tequila_api_call()

travel_data = FlightData(teq_json)

price_dep_dict = travel_data.get_lowest_price()
sheety_parameters = sheety.get_parameters(teq_json, price_dep_dict)
sheety_response = sheety_api_call()
message = format_message()
twi.send_text(message)
