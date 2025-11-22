"""Utilities for generating AI-powered weather summaries."""
from __future__ import annotations

from openai import OpenAI

from src.config.settings import get_settings
from src.utils.exceptions import MissingAPIKeyError
from src.utils.weather_api import WeatherData


def _get_client() -> OpenAI:
    settings = get_settings()
    if not settings.has_openai_key:
        raise MissingAPIKeyError(
            "OPENAI_API_KEY is required to generate AI weather summaries."
        )
    return OpenAI(api_key=settings.openai_api_key)


def generate_weather_tip(data: WeatherData) -> str:
    """Return a friendly summary for the given weather conditions."""

    client = _get_client()
    content = (
        "You are a helpful weather assistant. Based on the metrics provided, "
        "write one or two short sentences with practical advice."
    )
    weather_context = (
        f"City: {data.city}\nTemperature: {data.temperature}°C\n"
        f"Feels Like: {data.feels_like}°C\nDescription: {data.description}\n"
        f"Humidity: {data.humidity}%\nWind Speed: {data.wind_speed} m/s\n"
        f"Precipitation (mm): {data.precipitation}"
    )

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": content,
            },
            {
                "role": "user",
                "content": weather_context,
            },
        ],
    )

    message = response.output[0].content[0].text  # type: ignore[attr-defined]
    return message.strip()
