import requests
import argparse
from datetime import datetime
import math
from rich import print
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

API_KEY = "bb98bf2f8428ad68257a92b595bfd52e"


def get_result(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(
            f"[bold red]Error fetching weather data for {city}: {e}[/bold red]")
        return None
    except ValueError as e:
        print(
            f"[bold red]Error parsing weather data for {city}: {e}[/bold red]")
        return None


def get_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(
            f"[bold red]Error fetching forecast data for {city}: {e}[/bold red]")
        return None
    except ValueError as e:
        print(
            f"[bold red]Error parsing forecast data for {city}: {e}[/bold red]")
        return None


def calculate_dew_point(temperature, humidity):
    # formula to calculate dew point
    a = 17.27
    b = 237.7
    c = ((a * temperature) / (b + temperature)) + math.log(humidity / 100.0)
    dew_point = (b * c) / (a - c)
    return dew_point


def calculate_feels_like_temperature(temperature, wind_speed):
    # Formula to calculate feels like temperature (wind chill)
    feels_like = 13.12 + 0.6215 * temperature - 11.37 * \
        wind_speed ** 0.16 + 0.3965 * temperature * wind_speed ** 0.16
    return feels_like


def display_weather(city, data):
    # Retrieve weather information
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    real_feel = calculate_feels_like_temperature(
        temperature, data["wind"]["speed"])
    min_temp = data["main"]["temp_min"]
    max_temp = data["main"]["temp_max"]
    pressure = data["main"]["pressure"]
    visibility = data["visibility"]
    wind_speed = data["wind"]["speed"]
    uv_index = data.get("uvi", "N/A")
    sunrise_time = datetime.fromtimestamp(
        data["sys"]["sunrise"]).strftime("%H:%M:%S")
    sunset_time = datetime.fromtimestamp(
        data["sys"]["sunset"]).strftime("%H:%M:%S")
    dew_point = calculate_dew_point(
        data["main"]["temp"], data["main"]["humidity"])
    weather_description = data["weather"][0]["description"]

    table = Table(show_header=True, header_style="bold #00FFFF")
    table.add_column("Location", style="bold #00FFFF")
    table.add_column("Temperature (°C)", style="bold #00FFFF")
    table.add_column("Humidity (%)", style="bold #00FFFF")
    table.add_column("Real Feel (°C)", style="bold #00FFFF")
    table.add_column("Minimum Temperature", style="dim")
    table.add_column("Maximum Temperature", style="dim")
    table.add_column("Pressure", style="dim")
    table.add_column("Dew Point", style="dim")
    table.add_column("Visibility", style="dim")
    table.add_column("Wind Speed", style="dim")
    table.add_column("UV Index", style="dim")
    table.add_column("Sunrise Time", style="dim")
    table.add_column("Sunset Time", style="dim")

    table.add_row(
        city,
        f"{temperature}°C",
        f"{humidity}%",
        f"{real_feel}°C",
        f"{min_temp}°C",
        f"{max_temp}°C",
        f"{pressure} hPa",
        f"{dew_point}°C",
        f"{visibility} meters",
        f"{wind_speed} m/s",
        uv_index,
        sunrise_time,
        sunset_time,
    )

    console = Console()

    current_time = datetime.now()
    sunrise_time = datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset_time = datetime.fromtimestamp(data["sys"]["sunset"])
    if current_time < sunrise_time or current_time > sunset_time:
        emoji = "🌙         "  # Night emoji
    elif "rain" in weather_description.lower():
        emoji = "🌧         "
    elif "cloud" in weather_description.lower():
        emoji = "🌥         "
    else:
        emoji = "🔆         "  # Default day emoji

    additional_panel = Panel(
        f"{city}\n{emoji} [bold #00FFFF]{temperature}°C[/bold #00FFFF]\nFeels like: [bold #00FFFF]{real_feel}°C[/bold #00FFFF]\n{weather_description}",
        title="Current Weather:",
        style="bold #FFFFFF",
        width=40,
        expand=False,
    )
    console.print(additional_panel, justify="center")

    console.print(
        Panel.fit(
            table,
            title=f"Detail Weather Information for {city}:",
            style="bold #FF69B4",
            padding=(0, 1, 0, 1),
        )
    )


def display_forecast(city, data):
    table = Table(show_header=True, header_style="bold #00FFFF")
    table.add_column("Date", style="bold #00FFFF")
    table.add_column("Time", style="bold #00FFFF")
    table.add_column("Temperature (°C)", style="bold #00FFFF")
    table.add_column("Weather", style="bold #00FFFF")

    for forecast in data["list"]:
        forecast_datetime = datetime.fromtimestamp(forecast["dt"])
        date = forecast_datetime.strftime("%Y-%m-%d")
        time = forecast_datetime.strftime("%H:%M:%S")
        temperature = forecast["main"]["temp"]
        weather_description = forecast["weather"][0]["description"]

        table.add_row(date, time, f"{temperature}°C", weather_description)

    console = Console()
    console.print(
        Panel.fit(
            table,
            title=f"Weather Forecast for {city}:",
            style="bold #FF69B4",
            padding=(0, 1, 0, 1),
        )
    )


def generate_funny_tip(condition):
    if "rain" in condition.lower():
        return "The sky is about to cry. Better grab your umbrella and some tissues! 🌧"
    elif "cloud" in condition.lower():
        return "Cloudy skies ahead. Stay cozy indoors with a good book! 🌥"
    elif "clear" in condition.lower():
        return "The sky is clear. Grab a telescope and search for aliens! 🔭"
    elif "snow" in condition.lower():
        return "Bundle up and stay warm! ⛄️"
    else:
        return "Enjoy the beautiful weather! 🌈"


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
    parser = argparse.ArgumentParser(
        description="Get the current weather for a city")
    parser.add_argument("cities", metavar="city", nargs="+",
                        help="City name(s) for weather forecast")
    parser.add_argument("-f", "--forecast", action="store_true",
                        help="Display weather forecast for multiple days")

    args = parser.parse_args()
    cities = args.cities
    user_location_temp = get_result("Puri")["main"]["temp"]

    if args.forecast:
        for city in cities:
            forecast_data = get_forecast(city)
            if forecast_data:
                print("Weather forecast for", city + ":")
                display_forecast(city, forecast_data)
                print()
    else:
        for city in cities:
            weather_data = get_result(city)

            if weather_data:
                console = Console()

                display_weather(city, weather_data)

                temp_difference = calculate_temperature_difference(
                    user_location_temp, weather_data["main"]["temp"])
                console.print(
                    Panel(temp_difference, title="Temperature Difference:", style="#E6E6FA"))

                funny_tip = generate_funny_tip(
                    weather_data["weather"][0]["description"])
                console.print(
                    Panel(funny_tip, title="Funny Tip:", style="bold #FF69B4"))

                sunset_time = datetime.fromtimestamp(
                    weather_data["sys"]["sunset"])
                console.print(Panel(calculate_time_remaining(
                    sunset_time), title="Time Remaining Until Sunset:", style="bold #E6E6FA"))

                sunrise_time = datetime.fromtimestamp(
                    weather_data["sys"]["sunrise"])
                console.print(Panel(calculate_time_after_sunrise(
                    sunrise_time), title="Time After Sunrise:", style="bold #FF69B4"))

            else:
                print()


if __name__ == "__main__":
    main()
