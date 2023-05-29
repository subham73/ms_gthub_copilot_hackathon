import requests
from textual.app import App
from textual.widgets import Placeholder
# from textual.widgets import Window


class WeatherApp(App):
    async def on_mount(self, *args, **kwargs):
        self.add_window(WeatherWindow())

class WeatherWindow():
    def __init__(self):
        super().__init__(title="Weather")

        self.placeholder = Placeholder(
            "Enter your city name",
            on_change=self.on_change,
            style="bg:#333",
        )

        self.add(self.placeholder)

    async def on_change(self, value):
        if value:
            url = f"https://wttr.in/{value}?format=%C\n%t\n"
            response = requests.get(url)
            self.placeholder.text = response.text

if __name__ == "__main__":
    WeatherApp.run()