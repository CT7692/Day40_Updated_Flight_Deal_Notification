#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from flight_data import FlightData
from security import safe_requests
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import requests
import html


FONT_SIZE = 12
def format_message(pd_dict, iata_dict, dest, c_list):
    layovers = len(c_list)
    my_message = (f'Only ${pd_dict["price"]}'
               f' to fly from Saint Louis-STL to {dest}-'
               f'{iata_dict[dest]} on {pd_dict["departure"]}.\n\nFlight has {layovers}'
                  f' layovers in ')
    for city in c_list:
        if city == c_list[-1] and layovers >=2:
            my_message += f"and {city}."
        elif city != c_list[-1] and layovers >= 3:
            my_message += f"{city}, "
        else:
            my_message += f"{city} "
    return  my_message

def search_flights_and_send(city_cbox, destination, iata_dict, s_json, m_window, n_window, sending_addr):
    if city_cbox.current() == -1:
        messagebox.showwarning(title="Error", message="Please select a destination.")
    else:
        teq_parameters = (
            tequila.get_post_parameters(iata_dict[destination]))
        teq_response = tequila.api_call(teq_parameters)
        teq_json = teq_response.json()
        travel_data = FlightData(teq_json)
        price_dep_dict = travel_data.get_price_and_date()
        desired_dict = {
            destination: iata_dict[destination]
        }
        desired_price = s_json[sheety.flight_sheet][city_cbox.current()][sheety.lowest_price]
        if int(price_dep_dict["price"]) < desired_price:
            city_list = get_city_stops(travel_data, price_dep_dict)
            message = format_message(price_dep_dict, iata_dict, destination, city_list)
            try:
               gmail_obj.send_email(message, sending_addr)
            except Exception as err:
               messagebox.showerror(title="Error", message=err)
            else:
                messagebox.showinfo(title="Complete", message="Email sent.")
        n_window.quit()
        m_window.quit()



def register_user(main_window):
    first_name = first_name_text.get()
    last_name = last_name_text.get()
    email = email_text.get()
    confirmation = confirm_text.get()

    if email != confirmation:
        messagebox.showwarning(title="Error", message="The emails do not match. Please try again.")
    elif len(first_name) == 0 or len(last_name) == 0 or len(email) == 0 or len(confirmation) == 0:
        messagebox.showwarning(title="Error", message="All fields are required. Please try again.")
    else:
        user_parameters = {
            sheety.user_sheet: {
                "firstName": first_name,
                "lastName": last_name,
                "email": email
            }
        }

        response = sheety.api_post(sheety.user_sheet_endpoint, user_parameters)

        first_name_text.delete(0, END)
        last_name_text.delete(0, END)
        email_text.delete(0, END)
        confirm_text.delete(0, END)

        check_msg = messagebox.askyesno(title="Check Flights", message="Check for flight deals?")
        if check_msg:
            new_window = Tk()
            new_window.title("Select Destination")
            new_window.config(padx=20, pady=20)
            new_canvas = Canvas(width=400, height=400, highlightthickness=0)
            sheet = sheety.api_get(sheety.flight_sheet_endpoint)
            sheet.raise_for_status()
            sheet_json = sheet.json()
            tequila.get_iata_codes(sheet_json)
            city_cbox = ttk.Combobox(new_window, width=30)
            dest_dict = {}
            for option in sheet_json[sheety.flight_sheet]:
                dest_dict[option['city']] = option['iataCode']
            city_cbox['values'] = tuple(dest_dict)
            city_cbox.grid(column= 1, row=1, pady=3)
            select_destination = Button(
                new_window,text="Select", width=5,
                command=lambda: search_flights_and_send(
                    city_cbox,city_cbox.get(), dest_dict, sheet_json, main_window, new_window, email))
            select_destination.grid(column=1, row=2, pady=3)
        else:
            new_window.quit()
            main_window.quit()

def get_city_stops(t_data, pd_dict):
    city_list = []
    data = t_data.json["data"]
    for entry in data[pd_dict["index"]]["route"]:
        if entry['cityTo'] != t_data.city:
            city_list.append(entry['cityTo'])
    return city_list


tequila = FlightSearch()
sheety = DataManager()
gmail_obj = NotificationManager()

window = Tk()
window.title("User Registration")
window.config(padx=20, pady=20)
my_canvas = Canvas(width=250, height=250, highlightthickness=0)

first_name_label = Label(text="First Name: ", font=("Arial", FONT_SIZE))
first_name_label.grid(column=0, row=1, pady=3)

first_name_text = Entry(width=30)
first_name_text.grid(column=1, row=1, pady=3)

last_name_label = Label(text="Last Name: ", font=("Arial", FONT_SIZE))
last_name_label.grid(column=0, row=2, pady=3)

last_name_text = Entry(width=30)
last_name_text.grid(column=1, row=2, pady=3)

email_label = Label(text="Email: ", font=("Arial", FONT_SIZE))
email_label.grid(column=0, row=3, pady=3)

email_text = Entry(width=30)
email_text.grid(column=1, row=3, pady=3)

confirm_label = Label(text="Confirm Email: ", font=("Arial", FONT_SIZE))
confirm_label.grid(column=0, row=4, pady=3)

confirm_text = Entry(width=30)
confirm_text.grid(column=1, row=4, pady=3)

reg_button = Button(text="Register", width=15, command=lambda: register_user(window))
reg_button.grid(column=1, row=5, columnspan=2, pady=5)
first_name_text.focus()
window.mainloop()

