import requests
import argparse

API_KEY = "bb98bf2f8428ad68257a92b595bfd52e"


def get_result(city):
    CITY = city

    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # print(f"Current temperature in {CITY}: {data['main']['temp']}°C")
        return data
    else:
        # print("Error fetching weather data")
        return None


def display_weather(city, data):
    temperature = data['main']['temp']
    print(f"Current temperature in {city}: {temperature}°C")


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

    for city in args.cities:
        weather_data = get_result(city)

        if weather_data:
            display_weather(city, weather_data)

            user_location_temp = get_result("Puri")['main']['temp']
            temp_difference = calculate_temperature_difference(
                user_location_temp, weather_data['main']['temp'])
            print(temp_difference)

            funny_tip = generate_funny_tip(
                weather_data['weather'][0]['description'])
            print(funny_tip)
        else:
            print(f"Error fetching weather data for {city}.")


if __name__ == '__main__':
    main()
