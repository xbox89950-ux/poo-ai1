"""Weather information using OpenWeatherMap"""
import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)
API_KEY = "YOUR_OPENWEATHER_API_KEY"  # Replace with real key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

class Weather:
    @staticmethod
    def get_weather(city: str = "Dhaka") -> str:
        if API_KEY == "YOUR_OPENWEATHER_API_KEY":
            return "Please set OpenWeatherMap API key in modules/weather.py"
        try:
            params = {"q": city, "appid": API_KEY, "units": "metric"}
            r = requests.get(BASE_URL, params=params, timeout=10)
            data = r.json()
            if data.get("cod") != 200:
                return f"Error: {data.get('message', 'Unknown error')}"
            temp = data["main"]["temp"]
            feels = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            desc = data["weather"][0]["description"]
            return f"Weather in {city}: {temp}°C (feels like {feels}°C), {desc}, Humidity: {humidity}%"
        except Exception as e:
            return f"Weather error: {e}"

    @staticmethod
    def get_forecast(city: str = "Dhaka") -> str:
        if API_KEY == "YOUR_OPENWEATHER_API_KEY":
            return "Please set OpenWeatherMap API key"
        try:
            url = "https://api.openweathermap.org/data/2.5/forecast"
            params = {"q": city, "appid": API_KEY, "units": "metric", "cnt": 5}
            r = requests.get(url, params=params, timeout=10)
            data = r.json()
            if data.get("cod") != "200":
                return f"Error: {data.get('message')}"
            lines = [f"5-Day Forecast for {city}:"]
            for item in data["list"]:
                dt = item["dt_txt"]
                temp = item["main"]["temp"]
                desc = item["weather"][0]["description"]
                lines.append(f"  {dt}: {temp}°C, {desc}")
            return "\n".join(lines)
        except Exception as e:
            return f"Forecast error: {e}"
