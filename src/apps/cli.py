"""Project CLI entry point (Prompt 10)."""
from __future__ import annotations

import argparse
import logging
from typing import List

from src.utils import WeatherAPI, WeatherError, configure_logging


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Weather CLI powered by OpenWeatherMap")
    parser.add_argument("city", help="City name to query")
    parser.add_argument("--units", choices=["metric", "imperial"], help="Override temperature units")
    parser.add_argument("--lang", help="Override response language")
    parser.add_argument("--debug", action="store_true", help="Enable verbose logging")
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    logger = configure_logging(logging.DEBUG if args.debug else logging.INFO)
    api = WeatherAPI(units=args.units, language=args.lang)

    try:
        data = api.get_current_weather(args.city)
    except WeatherError as exc:
        logger.error("Failed to fetch weather: %s", exc)
        return 1

    logger.info(
        "%s: %s, Temp %.1f°, Feels %.1f°, Humidity %d%%",
        data.city,
        data.description,
        data.temperature,
        data.feels_like,
        data.humidity,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
