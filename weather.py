#Note: This piepline queries the 'OpenWeatherMap One Call API 3.0' to extract weather data based
#on latitude and longitude. In order to access this API you will need to create an account on 'https://openweathermap.org/api'
#and get an API key.

#Importing necessary libraries
import os
import requests
import configparser
import json
import sqlalchemy as sa
import pandas as pd
from dotenv import load_dotenv
from datetime import date

#Instantiating a ConfigParser and read the 'cites.cfg' file 
city_config = configparser.ConfigParser()
city_config.read('cities.cfg')

#Load from '.env' file and capture environment variables 
load_dotenv()
#Store the environment variables
API_KEY = os.environ['API_KEY']
PG_USER = os.environ['PG_USER']
PG_PASSWORD = os.environ['PG_PASSWORD']
PORT = os.environ['PORT']
DB = os.environ['DB']

#Test data for API queries
# lat = 40.6782
# lon = -73.9442
# url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={API_KEY}&units=imperial'

# Bklyn = {
#     'city': 'Brooklyn, NY',
#     'lat':40.6782,
#     'long': -73.9442
# }
# Mesa = {
#     'city': 'Mesa, AZ',
#     'lat':33.4152,
#     'long': -111.8315
# }
#Test driver code to see queried JSON data structure
#print(json.dumps(json.loads(requests.get(url).text), indent=4))

# test_array = [Bklyn, Mesa]

#Parse the city_config object into an array of location dictionaries
def parse_config():
    array = []
    for key, value in city_config['Cities'].items():
        if key[:4].lower() == 'city':
            temp = {
                'city': value,
                'lat': 0,
                'long': 0
            }
        elif key[:9].lower() == 'lattitude':
            temp['lat'] = float(value)
        elif key[:9].lower() == 'longitude':
            temp['long'] = float(value)
            array.append(temp)
    return array

#Use an array of location dictionaries to extract data by querying the API
def extract_data(loc_arr):
    raw_data = []
    for loc in loc_arr:
        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={loc['lat']}&lon={loc['long']}&exclude=current,minutely,hourly,alerts&appid={API_KEY}&units=imperial'
        #Wrapped in a 'try except' in the case of an exception the loop bypasses appending data to the extracted data array
        try:
            parsed = json.loads(requests.get(url).text)
        except:
            continue
        city = loc['city']
        raw_forecast_data = {
            'city':city,
            'parsed':parsed
        }
        raw_data.append(raw_forecast_data)

    return raw_data

#Transform the raw data into a 
def transform_data(data):
    weather_data = {
        'city' : [],
        'date' : [],
        'weather' : [],
        'temp_high': [],
        'temp_low': [],
        'temp_avg': [],
        'humidity' : []
    }
    for loc in data:
        loc_temp = loc['parsed']['daily'][0]['temp']
        weather_data['city'].append(loc['city'])
        weather_data['weather'].append(loc['parsed']['daily'][0]['weather'][0]['main'])
        weather_data['temp_high'].append(loc_temp['max'])
        weather_data['temp_low'].append(loc_temp['min'])
        weather_data['humidity'].append(loc['parsed']['daily'][0]['humidity'])
        weather_data['date'].append(date.today().strftime('%Y-%m-%d'))
        avg_temp = round((loc_temp['morn'] + loc_temp['night'] + loc_temp['eve'])/3,2)
        weather_data['temp_avg'].append(avg_temp)
    return weather_data


def load_data(data):
    df = pd.DataFrame(data)
    engine = sa.create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@localhost:{PORT}/{DB}')
    df.to_sql('weather_data',engine,if_exists='append',index=False)
    engine.dispose()



load_data(transform_data(extract_data(parse_config())))