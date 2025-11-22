"""Weather app with geolocation and hourly forecast (Prompt 7)."""
from __future__ import annotations

from datetime import datetime

from rich.console import Console
from rich.table import Table

from src.utils import (
    WeatherAPI,
    WeatherError,
    LocationDetectionError,
    detect_city,
)

console = Console()
API = WeatherAPI()


def format_hourly(city: str, hours: int = 12) -> None:
    try:
        forecast = API.get_hourly_forecast(city, hours=hours)
    except WeatherError as exc:
        console.print(f"Unable to fetch hourly forecast: {exc}", style="red")
        return

    table = Table(title=f"Next {hours} Hours in {city}")
    table.add_column("Time")
    table.add_column("Temp (°C)")
    table.add_column("Feels Like")
    table.add_column("Description")

    for entry in forecast:
        table.add_row(
            datetime.fromtimestamp(entry.timestamp).strftime("%H:%M"),
            f"{entry.temperature:.1f}",
            f"{entry.feels_like:.1f}",
            entry.description.title(),
        )
    console.print(table)


def main() -> None:
    console.print("Attempting to detect your location...", style="cyan")
    try:
        city = detect_city()
        console.print(f"Detected city: [bold green]{city}[/bold green]")
    except LocationDetectionError:
        console.print("Could not detect location. Please enter a city manually.", style="yellow")
        city = input("City: ").strip()

    if not city:
        console.print("City is required to continue.", style="red")
        return

    try:
        data = API.get_current_weather(city)
    except WeatherError as exc:
        console.print(f"Error fetching weather: {exc}", style="red")
        return

    console.print(
        f"[bold blue]{data.city}[/bold blue]: {data.description.title()}, "
        f"Temp {data.temperature:.1f}°C, Feels {data.feels_like:.1f}°C, Wind {data.wind_speed:.1f} m/s",
    )
    format_hourly(data.city)


if __name__ == "__main__":
    main()
