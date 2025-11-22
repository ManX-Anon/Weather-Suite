"""Wrapper around the OpenWeatherMap API."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

from src.config.settings import Settings, get_settings
from src.utils.exceptions import (
    MissingAPIKeyError,
    NetworkError,
    WeatherAPIError,
)


@dataclass(slots=True)
class WeatherData:
    city: str
    temperature: float
    feels_like: float
    pressure: int
    humidity: int
    wind_speed: float
    description: str
    icon: str
    sunrise: int
    sunset: int
    clouds: int
    precipitation: float

    @property
    def sunrise_time(self) -> datetime:
        return datetime.fromtimestamp(self.sunrise)

    @property
    def sunset_time(self) -> datetime:
        return datetime.fromtimestamp(self.sunset)


@dataclass(slots=True)
class ForecastEntry:
    timestamp: int
    temperature: float
    feels_like: float
    description: str
    icon: str

    @property
    def time(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp)


class WeatherAPI:
    """Simple OpenWeatherMap API client."""

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(
        self,
        settings: Optional[Settings] = None,
        session: Optional[requests.Session] = None,
        units: Optional[str] = None,
        language: Optional[str] = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.session = session or requests.Session()
        self.units = units or self.settings.default_units
        self.language = language or self.settings.language

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------
    def get_current_weather(
        self,
        city: str,
        *,
        units: Optional[str] = None,
        lang: Optional[str] = None,
    ) -> WeatherData:
        payload = self._request("weather", {"q": city}, units=units, lang=lang)
        return self._parse_current(payload)

    def get_hourly_forecast(
        self,
        city: str,
        hours: int = 12,
        *,
        units: Optional[str] = None,
        lang: Optional[str] = None,
    ) -> List[ForecastEntry]:
        payload = self._request("forecast", {"q": city}, units=units, lang=lang)
        entries = [self._parse_forecast_entry(item) for item in payload.get("list", [])]
        return entries[:hours]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _request(
        self,
        endpoint: str,
        params: Dict[str, Any],
        *,
        units: Optional[str] = None,
        lang: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not self.settings.has_openweather_key:
            raise MissingAPIKeyError(
                "OPENWEATHER_API_KEY is required. Provide it via environment variables or .env file."
            )

        request_params = {
            "appid": self.settings.openweather_api_key,
            "units": units or self.units,
            "lang": lang or self.language,
            **params,
        }

        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=request_params, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise NetworkError("Unable to reach OpenWeatherMap.") from exc

        payload = response.json()
        if response.status_code >= 400 or payload.get("cod") not in (200, "200"):
            message = payload.get("message", "Unknown error")
            raise WeatherAPIError(message)
        return payload

    @staticmethod
    def _parse_current(payload: Dict[str, Any]) -> WeatherData:
        weather = payload.get("weather", [{}])[0]
        main = payload.get("main", {})
        wind = payload.get("wind", {})
        sys_info = payload.get("sys", {})
        rain = payload.get("rain", {})
        snow = payload.get("snow", {})
        precipitation = rain.get("1h") or rain.get("3h") or snow.get("1h") or snow.get("3h") or 0.0

        return WeatherData(
            city=payload.get("name", "Unknown"),
            temperature=float(main.get("temp", 0.0)),
            feels_like=float(main.get("feels_like", 0.0)),
            pressure=int(main.get("pressure", 0)),
            humidity=int(main.get("humidity", 0)),
            wind_speed=float(wind.get("speed", 0.0)),
            description=weather.get("description", ""),
            icon=weather.get("icon", "01d"),
            sunrise=int(sys_info.get("sunrise", 0)),
            sunset=int(sys_info.get("sunset", 0)),
            clouds=int(payload.get("clouds", {}).get("all", 0)),
            precipitation=float(precipitation),
        )

    @staticmethod
    def _parse_forecast_entry(payload: Dict[str, Any]) -> ForecastEntry:
        weather = payload.get("weather", [{}])[0]
        main = payload.get("main", {})
        return ForecastEntry(
            timestamp=int(payload.get("dt", 0)),
            temperature=float(main.get("temp", 0.0)),
            feels_like=float(main.get("feels_like", 0.0)),
            description=weather.get("description", ""),
            icon=weather.get("icon", "01d"),
        )
