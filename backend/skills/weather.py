"""Weather skill — fetches current weather using Open-Meteo API (free, no key needed)."""

import os

import aiohttp

from skills.base import Skill


class WeatherSkill(Skill):
    name = "get_weather"
    description = "Get the current weather for a location"

    # Default location (can be overridden in .env)
    # User can set WEATHER_LAT and WEATHER_LON in .env

    def get_tool_definition(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": (
                    "Get the current weather conditions including temperature, "
                    "description, and if it will rain today. Use this when the "
                    "child asks about the weather."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        }

    async def execute(self, **kwargs) -> str:
        """Fetch current weather from Open-Meteo."""
        lat = os.environ.get("WEATHER_LAT", "40.7128")  # Default: NYC
        lon = os.environ.get("WEATHER_LON", "-74.0060")

        try:
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}"
                f"&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
                f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
                f"&temperature_unit=fahrenheit"
                f"&wind_speed_unit=mph"
                f"&timezone=auto"
                f"&forecast_days=1"
            )

            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status != 200:
                        return "I couldn't check the weather right now. Try again later!"
                    data = await resp.json()

            current = data.get("current", {})
            daily = data.get("daily", {})

            temp = current.get("temperature_2m", "?")
            humidity = current.get("relative_humidity_2m", "?")
            wind = current.get("wind_speed_10m", "?")
            weather_code = current.get("weather_code", 0)

            high = daily.get("temperature_2m_max", [None])[0]
            low = daily.get("temperature_2m_min", [None])[0]
            rain_chance = daily.get("precipitation_probability_max", [None])[0]

            # Convert WMO weather codes to child-friendly descriptions
            weather_desc = self._weather_code_to_description(weather_code)

            result = f"Right now it's {temp}\u00b0F and {weather_desc}. "
            if high and low:
                result += f"Today's high is {high}\u00b0F and the low is {low}\u00b0F. "
            if rain_chance is not None and rain_chance > 30:
                result += f"There's a {rain_chance}% chance of rain — maybe grab an umbrella! "
            elif rain_chance is not None:
                result += "No rain expected today! "

            return result

        except Exception as e:
            self.logger.error(f"Weather fetch failed: {e}")
            return "I couldn't check the weather right now, but I bet it's a great day!"

    def _weather_code_to_description(self, code: int) -> str:
        """Convert WMO weather code to a child-friendly description."""
        descriptions = {
            0: "clear and sunny",
            1: "mostly clear",
            2: "partly cloudy",
            3: "cloudy",
            45: "foggy",
            48: "foggy",
            51: "lightly drizzling",
            53: "drizzling",
            55: "drizzling a lot",
            61: "raining a little",
            63: "raining",
            65: "raining a lot",
            71: "snowing a little",
            73: "snowing",
            75: "snowing a lot",
            77: "snowing little ice bits",
            80: "having light rain showers",
            81: "having rain showers",
            82: "having heavy rain showers",
            85: "having light snow showers",
            86: "having heavy snow showers",
            95: "thunderstorming",
            96: "thunderstorming with hail",
            99: "thunderstorming with lots of hail",
        }
        return descriptions.get(code, "looking interesting outside")


def create_skill():
    return WeatherSkill()
