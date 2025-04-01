import requests
import os
from dotenv import load_dotenv
import json
from datetime import date
import pandas as pd

load_dotenv()

API_KEY = os.environ['API_KEY']

'''
lat = 40.6782
lon = -73.9442
url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclusion}&appid={API_KEY}&units={units}'
'''

def get_weather_data(lat, lon):
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={API_KEY}&units=imperial'
    weather_data_json = json.loads(requests.get(url).text)
    return weather_data_json

def extract_data():
    BklynNY = (40.6782, -73.9442)
    MesaAZ = (33.4152, -111.8315)
    YellowknifeCA = (62.4540, -114.3718)

    weather_data = {
        'Brooklyn': get_weather_data(BklynNY[0], BklynNY[1]),
        'Mesa': get_weather_data(MesaAZ[0], MesaAZ[1]),
        'Yellowknife' : get_weather_data(YellowknifeCA[0],YellowknifeCA[1])
    }

    return weather_data


def transform_weather_data(data):
    today = date.today().strftime('%Y-%m-%d')

    



