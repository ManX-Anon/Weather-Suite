"""Voice-controlled weather app (Prompt 8)."""
from __future__ import annotations

import speech_recognition as sr
import pyttsx3

from src.utils import WeatherAPI, WeatherError, VoiceInputError

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text: str) -> None:
    engine.say(text)
    engine.runAndWait()


def listen_for_city() -> str:
    with sr.Microphone() as source:
        speak("Please say the city name")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError as exc:
        raise VoiceInputError("Could not understand audio.") from exc
    except sr.RequestError as exc:
        raise VoiceInputError("Speech API unavailable.") from exc


def main() -> None:
    api = WeatherAPI()
    try:
        city = listen_for_city()
    except VoiceInputError as exc:
        speak(str(exc))
        return

    speak(f"Fetching weather for {city}")
    try:
        data = api.get_current_weather(city)
    except WeatherError as exc:
        speak(f"Error fetching weather: {exc}")
        return

    speak(
        f"Weather in {data.city}: {data.description}. Temperature {data.temperature:.1f} degrees, "
        f"feels like {data.feels_like:.1f}. Humidity {data.humidity} percent. Wind {data.wind_speed:.1f} meters per second."
    )


if __name__ == "__main__":
    main()
