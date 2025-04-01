import requests
import os
from dotenv import load_dotenv
import json
from datetime import date
import pandas as pd
import psycopg2

load_dotenv()

API_KEY = os.environ['API_KEY']


lat = 40.6782
lon = -73.9442
url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={API_KEY}&units=imperial'

Bklyn = {
    'lat':lat,
    'long': lon
}

def extract_data(loc):
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={loc['lat']}&lon={loc['long']}&exclude=current,minutely,hourly,alerts&appid={API_KEY}&units=imperial'
    parsed = json.loads(requests.get(url).text)
    # weather_data_json = json.dumps(parsed, indent=4)
    return parsed

def transform_data(data):
    weather_type = data['daily'][0]['weather'][0]['main']
    high = data['daily'][0]['temp']['max']
    low = data['daily'][0]['temp']['min']
    humidity = data['daily'][0]['humidity']
    weather_data = {
        'date' : [date.today().strftime('%Y-%m-%d')],
        'timezone' : [data['timezone']],
        'weather' : [weather_type],
        'temp high': [high],
        'temp low': [low],
        'temp avg': [(high+low)/2],
        'humidity' : [humidity]
    }
    return weather_data

def load_data(data):
    df = pd.DataFrame(data)
    




