"""Basic terminal weather application (Prompt 1)."""
from __future__ import annotations

import sys
from typing import Optional

from src.utils import WeatherAPI, WeatherError, configure_logging

logger = configure_logging()


def fetch_weather(city: str) -> None:
    api = WeatherAPI()
    try:
        data = api.get_current_weather(city)
    except WeatherError as exc:
        logger.error("Unable to fetch weather: %s", exc)
        print(f"Error: {exc}")
        return

    print("\nWeather for", data.city)
    print("-" * 30)
    print(f"Temperature : {data.temperature:.1f} °C")
    print(f"Humidity    : {data.humidity}%")
    print(f"Description : {data.description.title()}")
    print(f"Wind Speed  : {data.wind_speed:.1f} m/s")


def main(args: Optional[list[str]] = None) -> None:
    args = args or sys.argv[1:]
    if args:
        city = " ".join(args)
    else:
        city = input("Enter a city name: ").strip()

    if not city:
        print("Please provide a valid city name.")
        return

    fetch_weather(city)


if __name__ == "__main__":
    main()
