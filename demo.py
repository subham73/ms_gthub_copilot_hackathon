import requests
import argparse
from datetime import datetime
import math


API_KEY = "bb98bf2f8428ad68257a92b595bfd52e"


def get_result(city):
    CITY = city

    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data for {city}: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing weather data for {city}: {e}")
        return None


def calculate_dew_point(temperature, humidity):
    # formula to calculate dew point
    a = 17.27
    b = 237.7
    c = ((a * temperature) / (b + temperature)) + \
        math.log(humidity / 100.0)
    dew_point = (b * c) / (a - c)
    return dew_point


def calculate_feels_like_temperature(temperature, humidity, wind_speed):
    # formula to calculate feels like temperature
    c1 = -8.78469475556
    c2 = 1.61139411
    c3 = 2.33854883889
    c4 = -0.14611605
    c5 = -0.012308094
    c6 = -0.0164248277778
    c7 = 0.002211732
    c8 = 0.00072546
    c9 = -0.000003582
    feels_like = c1 + c2 * temperature + c3 * humidity + c4 * temperature * humidity + c5 * temperature**2 + c6 * \
        humidity**2 + c7 * temperature**2 * humidity + c8 * \
        temperature * humidity**2 + c9 * temperature**2 * humidity**2

    if wind_speed > 4.8:
        feels_like -= ((wind_speed - 4.8) / 10)

    return feels_like



def display_weather(city, data):
    temperature = data['main']['temp']
    min_temp = data['main']['temp_min']
    max_temp = data['main']['temp_max']
    # temperatures = []
    # temperatures.append(temperature)
    # min_temp = min(item['main']['temp'] for item in data['list'])
    # max_temp = max(item['main']['temp'] for item in data['list'])
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    visibility = data['visibility']
    wind_speed = data['wind']['speed']
    uv_index = data.get('uvi', 'N/A')

    dew_point = calculate_dew_point(temperature, humidity)
    feels_like = calculate_feels_like_temperature(
        temperature, humidity, wind_speed)

    print(f"Current temperature in {city}: {temperature}°C")
    print(f"Feels Like: {feels_like}°C")
    print(f"Minimum temperature of the day: {min_temp}°C")
    print(f"Maximum temperature of the day: {max_temp}°C")

    # print(f"Minimum temperature of the day: {min(temperatures)}°C")
    # print(f"Maximum temperature of the day: {max(temperatures)}°C")
    print(f"Humidity: {humidity}%")
    print(f"Pressure: {pressure} hPa")
    print(f"Dew Point: {dew_point}°C")
    print(f"Visibility: {visibility} meters")
    print(f"Wind Speed: {wind_speed} m/s")
    print(f"UV Index: {uv_index}")

    temp_thresholds = {'lower': 10, 'upper': 30}
    humidity_thresholds = {'lower': 30, 'upper': 70}
    wind_speed_thresholds = {'lower': 5, 'upper': 15}

    temp_comments = {
        'lower': "It's a bit chilly today.",
        'in_range': "The temperature is pleasant.",
        'upper': "It's quite hot today."
    }
    humidity_comments = {
        'lower': "Humidity is low, enjoy the dry air.",
        'in_range': "Humidity is at a comfortable level.",
        'upper': "It's quite humid today."
    }
    wind_speed_comments = {
        'lower': "The wind is calm today.",
        'in_range': "Moderate wind speed.",
        'upper': "It's windy today."
    }

    temp_description = ""
    if temperature < temp_thresholds['lower']:
        temp_description = temp_comments['lower']
    elif temperature > temp_thresholds['upper']:
        temp_description = temp_comments['upper']
    else:
        temp_description = temp_comments['in_range']

    humidity_description = ""
    if humidity < humidity_thresholds['lower']:
        humidity_description = humidity_comments['lower']
    elif humidity > humidity_thresholds['upper']:
        humidity_description = humidity_comments['upper']
    else:
        humidity_description = humidity_comments['in_range']

    wind_speed_description = ""
    if wind_speed < wind_speed_thresholds['lower']:
        wind_speed_description = wind_speed_comments['lower']
    elif wind_speed > wind_speed_thresholds['upper']:
        wind_speed_description = wind_speed_comments['upper']
    else:
        wind_speed_description = wind_speed_comments['in_range']

    print(
        f"Weather Description: {temp_description}, {humidity_description}, {wind_speed_description}")


def generate_funny_tip(condition):
    if "rain" in condition.lower():
        return "The sky is about to cry. Better grab your umbrella and some tissues!"
    elif "cloud" in condition.lower():
        return "Cloudy skies ahead. Don't forget your jacket!"
    elif "sunny" in condition.lower():
        return "It's sunny outside. Don't forget your sunscreen!"
    else:
        return "No funny tip available for this weather condition."


def calculate_temperature_difference(user_temp, typed_temp):
    diff = user_temp - typed_temp
    return f"Temperature difference: {abs(diff)}°C {'higher' if diff > 0 else 'lower'} than your location."


def calculate_time_remaining(sunset_time):
    now = datetime.now()
    time_remaining = sunset_time - now
    return f"Time remaining until sunset: {time_remaining}"


def calculate_time_after_sunrise(sunrise_time):
    now = datetime.now()
    time_after_sunrise = now - sunrise_time
    return f"Time after sunrise: {time_after_sunrise}"


def main():
    # get_result("delhi")
    #     parser = argparse.ArgumentParser(description='Get the current weather for a city')
    #     parser.add_argument('city', type=str, help='the name of the city')
    #     args = parser.parse_args ()

    #    get_result(city)
    parser = argparse.ArgumentParser(
        description='Get the current weather for a city')
    parser.add_argument('cities', metavar='city', nargs='+',
                        help='City name(s) for weather forecast')
    args = parser.parse_args()
    user_location_temp = get_result("Puri")['main']['temp']

    for city in args.cities:
        weather_data = get_result(city)

        if weather_data:
            display_weather(city, weather_data)
            temp_difference = calculate_temperature_difference(
                user_location_temp, weather_data['main']['temp'])
            print(temp_difference)

            funny_tip = generate_funny_tip(
                weather_data['weather'][0]['description'])
            print(funny_tip)

            sunset_time = datetime.fromtimestamp(weather_data['sys']['sunset'])
            print(calculate_time_remaining(sunset_time))

            sunrise_time = datetime.fromtimestamp(
                weather_data['sys']['sunrise'])
            print(calculate_time_after_sunrise(sunrise_time))

        else:
            print()


if __name__ == '__main__':
    main()
