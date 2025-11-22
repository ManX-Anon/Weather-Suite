"""FastAPI weather microservice (Prompt 6)."""
from __future__ import annotations

import time
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.utils import WeatherAPI, WeatherError

app = FastAPI(
    title="Weather Microservice",
    description="Production-ready FastAPI weather endpoint backed by OpenWeatherMap.",
    version="1.0.0",
)
api = WeatherAPI()


class WeatherResponse(BaseModel):
    city: str
    temp: float
    feels_like: float
    humidity: int
    precipitation: float
    clouds: int


class ErrorResponse(BaseModel):
    detail: str


def _cache_bucket() -> int:
    """Return a rolling bucket that changes every 5 minutes."""

    return int(time.time() // 300)


@lru_cache(maxsize=256)
def _cached_weather(city: str, bucket: int):
    return api.get_current_weather(city)


@app.get(
    "/weather/{city}",
    response_model=WeatherResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        404: {"model": ErrorResponse, "description": "City not found"},
    },
)
def weather(city: str):
    """Return weather data for the provided city."""

    bucket = _cache_bucket()
    try:
        data = _cached_weather(city.lower(), bucket)
    except WeatherError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return WeatherResponse(
        city=data.city,
        temp=data.temperature,
        feels_like=data.feels_like,
        humidity=data.humidity,
        precipitation=data.precipitation,
        clouds=data.clouds,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
