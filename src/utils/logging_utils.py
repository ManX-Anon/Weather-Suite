"""Logging helpers for the weather project."""
from __future__ import annotations

import logging
from typing import Optional


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure and return the root logger only once."""

    logger = logging.getLogger("weather_app")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
