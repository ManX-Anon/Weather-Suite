"""Advanced Rich-powered terminal weather app (Prompt 2)."""
from __future__ import annotations

from typing import Iterable

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.utils import WeatherAPI, WeatherError
from src.utils.rich_helpers import format_temperature

console = Console()


def render_city_weather(city: str) -> None:
    api = WeatherAPI()
    try:
        data = api.get_current_weather(city)
    except WeatherError as exc:
        console.print(Panel(str(exc), title=f"Error: {city}", border_style="red"))
        return

    rows = Table.grid(padding=(0, 2))
    rows.add_row("Temperature", format_temperature(data.temperature))
    rows.add_row("Feels Like", f"{data.feels_like:.1f}°C")
    rows.add_row("Pressure", f"{data.pressure} hPa")
    rows.add_row("Humidity", f"{data.humidity}%")
    rows.add_row("Sunrise", data.sunrise_time.strftime("%H:%M"))
    rows.add_row("Sunset", data.sunset_time.strftime("%H:%M"))

    console.print(
        Panel(
            rows,
            title=f"╭ Weather for {data.city} ╮",
            border_style="bright_blue",
        )
    )


def main() -> None:
    console.print("Enter city names separated by commas (e.g., Delhi, Mumbai, Pune)")
    raw = input("Cities: ")
    cities: Iterable[str] = (
        city.strip() for city in raw.split(",") if city.strip()
    )

    any_city = False
    for city in cities:
        any_city = True
        render_city_weather(city)
    if not any_city:
        console.print("No cities provided.", style="bold red")


if __name__ == "__main__":
    main()
