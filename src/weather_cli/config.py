"""Runtime configuration for the weather CLI.

Environment variables are read once at import time. Invalid values fall back
to the documented defaults so the CLI never fails because of a bad environment.

Attributes:
    GEO_URL: Open-Meteo geocoding endpoint.
    FORECAST_URL: Open-Meteo forecast endpoint.
    USER_AGENT: HTTP User-Agent sent with every request.
    DEFAULT_UNIT: Unit used when ``--unit`` is not supplied.
    TIMEOUT: HTTP timeout in seconds.
"""

from __future__ import annotations

import os

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
USER_AGENT = "priyanshkk-weather-cli/1.0"

VALID_UNITS = ("celsius", "fahrenheit")


def env_int(name: str, default: int, *, minimum: int = 1) -> int:
    """Read a bounded integer from the environment.

    Args:
        name: Environment variable name.
        default: Value to use when the variable is absent or invalid.
        minimum: Smallest accepted value.

    Returns:
        The parsed integer or ``default``.
    """
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return value if value >= minimum else default


def env_unit(name: str, default: str) -> str:
    """Read a temperature unit from the environment.

    Args:
        name: Environment variable name.
        default: Value to use when the variable is absent or unsupported.

    Returns:
        ``"celsius"`` or ``"fahrenheit"``.
    """
    value = os.environ.get(name, default).strip().lower()
    return value if value in VALID_UNITS else default


DEFAULT_UNIT = env_unit("WEATHER_UNIT", "celsius")
TIMEOUT = env_int("WEATHER_TIMEOUT", 10)

__all__ = ["DEFAULT_UNIT", "TIMEOUT", "env_int", "env_unit"]
