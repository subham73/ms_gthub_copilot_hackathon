import requests
import argparse

API_KEY = "bb98bf2f8428ad68257a92b595bfd52e"
def get_result(city):
    CITY = city

    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"Current temperature in {CITY}: {data['main']['temp']}°C")
    else:
        print("Error fetching weather data")

def main():
    get_result("delhi")
#     parser = argparse.ArgumentParser(description='Get the current weather for a city')
#     parser.add_argument('city', type=str, help='the name of the city')
#     args = parser.parse_args ()

#    get_result(city)

if __name__ == '__main__':
    main()     