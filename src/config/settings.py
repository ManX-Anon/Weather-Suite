"""Application-wide configuration utilities."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional

import os

#from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    # Fallback to environment variables already present in the shell.
    load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    openweather_api_key: str = os.getenv("OPENWEATHER_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    default_units: str = os.getenv("OPENWEATHER_UNITS", "metric")
    language: str = os.getenv("OPENWEATHER_LANG", "en")

    @property
    def has_openweather_key(self) -> bool:
        return bool(self.openweather_api_key)

    @property
    def has_openai_key(self) -> bool:
        return bool(self.openai_api_key)

    def require_openweather_key(self) -> None:
        if not self.has_openweather_key:
            raise RuntimeError(
                "Missing OpenWeatherMap API key. Set OPENWEATHER_API_KEY in your environment or .env file."
            )

    def require_openai_key(self) -> None:
        if not self.has_openai_key:
            raise RuntimeError(
                "Missing OpenAI API key. Set OPENAI_API_KEY in your environment or .env file."
            )


@lru_cache()
def get_settings() -> Settings:
    """Return a cached ``Settings`` instance."""

    return Settings()
