import requests
import os
from dotenv import load_dotenv
import json
from datetime import date
import pandas as pd

load_dotenv()
API_KEY = os.environ['API_KEY']


lat = 40.6782
lon = -73.9442
url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={API_KEY}&units=imperial'

Bklyn = {
    'city': 'Brooklyn, NY',
    'lat':40.6782,
    'long': -73.9442
}
Mesa = {
    'city': 'Mesa, AZ',
    'lat':33.4152,
    'long': -111.8315
}

#print(json.dumps(json.loads(requests.get(url).text), indent=4))

test_array = [Bklyn, Mesa]

def extract_data(loc_arr):
    raw_data = []
    for loc in loc_arr:
        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={loc['lat']}&lon={loc['long']}&exclude=current,minutely,hourly,alerts&appid={API_KEY}&units=imperial'
        parsed = json.loads(requests.get(url).text)
        city = loc['city']
        # weather_data_json = json.dumps(parsed, indent=4)
        raw_forecast_data = {
            'city':city,
            'parsed':parsed
        }
        raw_data.append(raw_forecast_data)

    return raw_data


def transform_data(data):
    weather_data = {
        'city' : [],
        'date' : [],
        'timezone' : [],
        'weather' : [],
        'temp high': [],
        'temp low': [],
        'temp avg': [],
        'humidity' : []
    }
    for loc in data:
        weather_data['city'].append(loc['city'])
        weather_data['weather'].append(loc['parsed']['daily'][0]['weather'][0]['main'])
        weather_data['temp high'].append(loc['parsed']['daily'][0]['temp']['max'])
        weather_data['temp low'].append(loc['parsed']['daily'][0]['temp']['min'])
        weather_data['humidity'].append(loc['parsed']['daily'][0]['humidity'])
        weather_data['timezone'].append(loc['parsed']['timezone'])
        weather_data['date'].append(date.today().strftime('%Y-%m-%d'))
        weather_data['temp avg'].append(loc['parsed']['daily'][0]['temp']['day'])
    return weather_data


def load_data(data):
    df = pd.DataFrame(data)
    return df
    
print(load_data(transform_data(extract_data(test_array))))




