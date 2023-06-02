"""This module provides the weahi model-controller."""

from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from datetime import datetime, timedelta

from heywea import DB_READ_ERROR, ID_ERROR, SUCCESS
from heywea.database import DatabaseHandler

# from  util.py import call_api
API_KEY = "bb98bf2f8428ad68257a92b595bfd52e"
import requests

def call_api(CITY):
    """call the openweather api."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    url2 = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    response2 = requests.get(url2)
    if response.status_code != 200 or response2.status_code != 200:
        return {}, {}
    data = response.json()
    data2 = response2.json()
    print(data)
    return data, data2


#structure of weather data 
class WeatherData(NamedTuple):
    data_block: Dict[str, Any]
    error: int

class DayWiseData:
    def __init__(self, db_path) -> None:
        self._db_handler = DatabaseHandler(db_path)
    
    #function to store weather data to database    
    def store_data(self, CITY, inp1: Dict[str, Any], inp2: Dict[str, Any] ) -> WeatherData:
        """store data to the database."""
        data_block = {
            "City" : CITY, 
            "Date" : datetime.now().strftime("%Y-%m-%d"),
            "Time" : datetime.now().strftime("%H:%M:%S"),
            "OneDayData": inp1,
            "FiveDayData": inp2
        } 
        
        read = self._db_handler.read_data()
        if read.error == DB_READ_ERROR:
            return WeatherData(data_block, read.error)
        read.data_list.append(data_block)
        write = self._db_handler.write_data(read.data_list)
        return WeatherData(data_block, write.error)

    #function to get weather data from database if date is same else call openweather api 
    #and store data to database and show the result
    def get_Weather_data(self, CITY) -> WeatherData:
        """get data from the database."""
        read = self._db_handler.read_data()
        if read.error == DB_READ_ERROR:
            return WeatherData({}, read.error)
        for i in range(len(read.data_list)):
            if read.data_list[i]["City"] == CITY and read.data_list[i]["Date"] == datetime.now().strftime("%Y-%m-%d"):
                return WeatherData(read.data_list[i], SUCCESS)
        inp1, inp2 = call_api(CITY)
        api_res = store_data(CITY, inp1, inp2)
        return api_res




    