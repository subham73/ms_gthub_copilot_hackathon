"""Top-level package for """

# create skeleton for a cli appication FOR weather app
__app_name__ = "Weather App"
__version__ = "0.1.0"

# define a series of return assign integer numbers to them using range()
(
    SUCCESS,
    ERROR
    

) = range(2)

ERROR ={
    "city_not_found": "City not found",
    "no_weather_data": "No weather data available",
    "no_funny_tip": "No funny tip available for this weather condition",
}