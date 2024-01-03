import os
class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, json_data):
        self.json = json_data
        self.city = self.json["data"][0]["cityTo"]
        self.airport = self.json["data"][0]["flyTo"]

    def get_lowest_price(self):
        i = 0
        low_price = self.json["data"][0]["price"]
        departure = self.json["data"][0]["local_departure"].split("T")[0]
        for row in self.json["data"]:
            current_price = self.json["data"][i]["price"]
            if current_price < low_price:
                low_price = current_price
                departure = self.json["data"][i]["local_departure"].split("T")[0]
            i += 1

        my_dict = {
            "price": low_price,
            "departure": departure
        }
        return my_dict