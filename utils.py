from rich.table import Table
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from rich import print

from artifacts import digital_digits, weather_arts
console = Console()



weather_data={'coord': {'lon': 86.6167, 'lat': 20.3167}, 
              'weather': [{'id': 802, 'main': 'Clouds', 
                           'description': 'scattered clouds', 'icon': '03d'}], 
            'base': 'stations', 'main': {'temp': 31.8, 'feels_like': 38.8, 
                                         'temp_min': 31.8, 'temp_max': 31.8, 
                                         'pressure': 1003, 'humidity': 68, 
                                         'sea_level': 1003, 'grnd_level': 1003},
             'visibility': 10000, 'wind': {'speed': 2.73, 'deg': 162, 'gust': 6.43}, 
             'clouds': {'all': 27}, 'dt': 1685877560, 
             'sys': {'country': 'IN', 'sunrise': 1685835178, 'sunset': 1685883051}, 
             'timezone': 19800, 'id': 1260393, 'name': 'Paradip', 'cod': 200}


def get_digital_digit(num):
    digi1 = digital_digits[num // 10]
    digi2 = digital_digits[num % 10]
    return digi1, digi2

def get_weather_art(description):
    #TODO
    #match the weather description with the weather_art
    #dummy output 
    return weather_arts["rain"]

def default(city, weather_data):
    weather_art = get_weather_art(weather_data['weather'][0]['main'])
    digi1, digi2 = get_digital_digit(int(weather_data['main']['temp']))
    #TOD: different units
    degree = f"[bold]{'°C'}"

    main_block = Panel(Columns([weather_art, digi1, digi2, degree]), 
                     width = 27, title = city, title_align='left')

    print(main_block)

# default("Paradip", weather_data)

#not completed
def detailed(city, weather_data):
    weather_art = get_weather_art(weather_data['weather'][0]['main'])
    digi1, digi2 = get_digital_digit(int(weather_data['main']['temp']))
    #TOD: different units
    degree = f"[bold]{'°C'}"

    main_block = Panel(Columns([weather_art, digi1, digi2, degree]), 
                     width = 27, title = city, title_align='left')

    feels_like = Columns(f"{'Feels :'}{weather_data['main']['feels_like']}")
    wind = f"🌀 {' Wind :'}{weather_data['wind']['speed']}"
    humidity = f"💦{' Humidity :'}{weather_data['main']['humidity']}"
    pressure = f"🪨 {' Pressure :'}{weather_data['main']['pressure']}"
    visibility = f"👓{' visibility :'}{weather_data['visibility']}"

    list = [feels_like, wind, humidity, pressure, visibility]
    
    user_renderables = Panel(Columns(list))

    col = Columns([main_block, user_renderables], equal = True)

    console.print(col, justify="center")
    
# detailed("Paradip", weather_data)