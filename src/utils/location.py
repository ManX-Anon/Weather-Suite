"""Location detection utilities."""
from __future__ import annotations

from typing import Optional

import geocoder

from src.utils.exceptions import LocationDetectionError


def detect_city() -> str:
    """Attempt to detect the user's city using geocoder."""

    try:
        g = geocoder.ip("me")
    except Exception as exc:
        raise LocationDetectionError("Could not contact geolocation service.") from exc

    if not g or not g.ok or not g.city:
        raise LocationDetectionError("Unable to detect current city automatically.")
    return g.city
