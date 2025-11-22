"""Custom exception types for weather applications."""


class WeatherError(Exception):
    """Base exception for recoverable weather-related issues."""


class MissingAPIKeyError(WeatherError):
    """Raised when an API call is attempted without an API key."""


class WeatherAPIError(WeatherError):
    """Raised when OpenWeatherMap returns an error response."""


class NetworkError(WeatherError):
    """Raised when a network request cannot be completed."""


class VoiceInputError(WeatherError):
    """Raised when voice input cannot be captured or recognized."""


class LocationDetectionError(WeatherError):
    """Raised when the user's location cannot be determined."""
