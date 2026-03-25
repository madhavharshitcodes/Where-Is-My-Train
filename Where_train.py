import tkinter as tk
from datetime import datetime

import requests

API_KEY = "qhx3wzhx26"
BASE_URL = "https://indianrailapi.com/api/v2/livetrainstatus"


root = tk.Tk()
root.geometry("1366x768")
root.title("Live Train Status")
root.config(bg="pink")

tk.Label(root, text="Live Train Status", width=20, font=("bold", 15), fg="brown", bg="pink").place(x=90, y=83)

tk.Label(root, text="Train Number : ", width=20, font=("bold", 10), fg="black", bg="pink").place(x=60, y=130)
numbers = tk.StringVar(value="Ex : 12056")
entry_1 = tk.Entry(root, textvariable=numbers)
entry_1.place(x=200, y=130)

tk.Label(root, text="Today's Date : ", width=20, font=("bold", 10), fg="black", bg="pink").place(x=60, y=160)
dates = tk.StringVar(value="Ex : 01-07-2018")
entry_2 = tk.Entry(root, textvariable=dates)
entry_2.place(x=200, y=160)


def set_output(train_name: str, source: str, destination: str, position: str) -> None:
    label_3.configure(text=train_name)
    label_4.configure(text=source)
    label_5.configure(text=destination)
    label_6.configure(text=position)


def to_api_date(input_date: str) -> str:
    return datetime.strptime(input_date, "%d-%m-%Y").strftime("%Y%m%d")


def live() -> None:
    train_number = entry_1.get().strip()
    current_date = entry_2.get().strip()

    if not train_number.isdigit():
        set_output("Invalid Input", "Train number must be digits", "", "")
        return

    try:
        api_date = to_api_date(current_date)
    except ValueError:
        set_output("Invalid Input", "Date must be DD-MM-YYYY", "", "")
        return

    complete_url = f"{BASE_URL}/apikey/{API_KEY}/trainnumber/{train_number}/date/{api_date}/"

    try:
        response = requests.get(complete_url, timeout=10)
        response.raise_for_status()
        result = response.json()

        if "response_code" in result:
            if result.get("response_code") != 200:
                set_output("API Error", "Request failed", "", "")
                return

            route = result.get("route", [])
            if not route:
                set_output("API Error", "No route data", "", "")
                return

            train_name = str(result.get("train", {}).get("name", "Unknown"))
            source_station = str(route[0].get("station", {}).get("name", "Unknown"))
            destination_station = str(route[-1].get("station", {}).get("name", "Unknown"))
            position = str(result.get("position", "Unknown"))
            set_output(train_name, source_station, destination_station, position)
            return

        response_code = str(result.get("ResponseCode", ""))
        if response_code != "200":
            message = str(result.get("Message", "API request failed"))
            set_output("API Error", message[:35], "", "")
            return

        train_name = str(result.get("TrainName") or result.get("Train") or "Train")
        source_station = str(result.get("Source") or result.get("StartStation") or "Unknown")
        destination_station = str(result.get("Destination") or result.get("EndStation") or "Unknown")
        position = str(
            result.get("CurrentStation")
            or result.get("Position")
            or result.get("TrainStatus")
            or "Live status received"
        )
        set_output(train_name, source_station, destination_station, position)
    except (requests.RequestException, ValueError, KeyError, TypeError):
        set_output("Network Error", "Unable to reach API", "Check internet/API key", "")


label_3 = tk.Label(root, text="...", width=30, font=("bold", 8), fg="black", bg="pink")
label_3.place(x=110, y=240)
label_4 = tk.Label(root, text="...", width=30, font=("bold", 8), fg="black", bg="pink")
label_4.place(x=110, y=260)
label_5 = tk.Label(root, text="...", width=30, font=("bold", 8), fg="black", bg="pink")
label_5.place(x=110, y=280)
label_6 = tk.Label(root, text="...", width=50, font=("bold", 8), fg="black", bg="pink")
label_6.place(x=50, y=300)

tk.Label(root, text="Indian Railway", width=20, font=("bold", 8), fg="black", bg="pink").place(x=140, y=340)
tk.Label(root, text="Developed by Shreekant Gosavi", width=30, font=("bold", 8), fg="black", bg="pink").place(x=110, y=360)

tk.Button(root, text="Show", width=20, bg="brown", fg="white", command=live).place(x=130, y=200)

root.mainloop()
