import os
import requests
import json
from typing import List, Tuple

import geocoder


# Define global variables
api_key: str
location: List[float]


# Retrieves OpenWeather API token and sets location of user
def init():
    global api_key, location

    print("--Initialising weather module--")

    api_key = os.environ['OPENWEATHER_API_TOKEN']
    location = geocoder.ip('me').latlng


# Retrieve current weahter data from current location
def get_current_weather():
    global api_key, location

    # generate URL
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (location[0], location[1], api_key)

    # request data from API
    response = requests.get(url)
    data = json.loads(response.text)
    return data['current']
