"""AI-powered weather assistant (Prompt 9)."""
from __future__ import annotations

from rich.console import Console
from rich.panel import Panel

from src.utils import WeatherAPI, WeatherError
from src.utils.openai_helper import generate_weather_tip

console = Console()


def main() -> None:
    city = input("Enter a city: ").strip()
    if not city:
        console.print("City is required.", style="bold red")
        return

    api = WeatherAPI()
    try:
        data = api.get_current_weather(city)
    except WeatherError as exc:
        console.print(f"Error fetching weather: {exc}", style="red")
        return

    console.print(
        Panel(
            f"Description: {data.description.title()}\n"
            f"Temperature: {data.temperature:.1f}°C (feels {data.feels_like:.1f}°C)\n"
            f"Humidity: {data.humidity}% | Wind: {data.wind_speed:.1f} m/s",
            title=f"Weather in {data.city}",
        )
    )

    try:
        tip = generate_weather_tip(data)
    except Exception as exc:  # broad to handle API issues
        console.print(f"AI tip unavailable: {exc}", style="yellow")
        return

    console.print(Panel(tip, title="AI Advice", border_style="green"))


if __name__ == "__main__":
    main()
