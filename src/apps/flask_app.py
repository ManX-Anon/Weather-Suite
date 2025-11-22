"""Flask weather web app (Prompt 5) now hosting unified landing page."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from flask import Flask, jsonify, render_template, request

from src.utils import WeatherAPI, WeatherError, detect_city
from src.utils.exceptions import LocationDetectionError
from src.utils.openai_helper import generate_weather_tip
from src.utils.weather_api import ForecastEntry, WeatherData

TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "templates"


def serialize_weather(data: WeatherData) -> Dict[str, Any]:
    return {
        "city": data.city,
        "temperature": data.temperature,
        "feels_like": data.feels_like,
        "pressure": data.pressure,
        "humidity": data.humidity,
        "wind_speed": data.wind_speed,
        "description": data.description,
        "sunrise": data.sunrise_time.strftime("%H:%M"),
        "sunset": data.sunset_time.strftime("%H:%M"),
        "icon": data.icon,
        "clouds": data.clouds,
    }


def serialize_forecast(entries: List[ForecastEntry]) -> List[Dict[str, Any]]:
    return [
        {
            "time": entry.time.strftime("%H:%M"),
            "temperature": entry.temperature,
            "feels_like": entry.feels_like,
            "description": entry.description,
            "icon": entry.icon,
        }
        for entry in entries
    ]


def create_app() -> Flask:
    app = Flask(__name__, template_folder=str(TEMPLATE_DIR))
    api = WeatherAPI()

    @app.get("/")
    def dashboard():
        return render_template("index.html")

    @app.get("/weather")
    def weather_endpoint():
        city = request.args.get("city", "").strip()
        if not city:
            return jsonify({"error": "City query parameter is required."}), 400
        try:
            data = api.get_current_weather(city)
        except WeatherError as exc:
            return jsonify({"error": str(exc)}), 400

        return jsonify(serialize_weather(data))

    @app.post("/multi-weather")
    def multi_weather():
        payload = request.get_json(silent=True) or {}
        cities = payload.get("cities", [])
        if not isinstance(cities, list) or not cities:
            return jsonify({"error": "Provide a non-empty list of cities."}), 400

        results = []
        for city in cities:
            city_name = str(city).strip()
            if not city_name:
                continue
            try:
                data = api.get_current_weather(city_name)
            except WeatherError as exc:
                results.append({"city": city_name, "error": str(exc)})
                continue
            results.append({"city": city_name, "data": serialize_weather(data)})
        return jsonify({"results": results})

    @app.get("/forecast")
    def forecast():
        city = request.args.get("city", "").strip()
        hours = min(int(request.args.get("hours", 6)), 12)
        if not city:
            try:
                city = detect_city()
            except LocationDetectionError as exc:
                return jsonify({"error": str(exc)}), 400

        try:
            entries = api.get_hourly_forecast(city, hours=hours)
        except WeatherError as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify({"city": city, "forecast": serialize_forecast(entries)})

    @app.post("/ai-advice")
    def ai_advice():
        payload = request.get_json(silent=True) or {}
        city = str(payload.get("city", "")).strip()
        if not city:
            return jsonify({"error": "City is required."}), 400
        try:
            data = api.get_current_weather(city)
        except WeatherError as exc:
            return jsonify({"error": str(exc)}), 400
        try:
            tip = generate_weather_tip(data)
        except Exception as exc:  # pragma: no cover - external API failure
            return jsonify({"error": f"AI service unavailable: {exc}"}), 502
        return jsonify({"city": city, "advice": tip})

    @app.get("/detect-city")
    def detect_city_endpoint():
        try:
            city = detect_city()
        except LocationDetectionError as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify({"city": city})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
