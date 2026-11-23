"""Open-Meteo requests and report formatting.

All HTTP access funnels through :func:`get_json`, which is the single seam the
tests patch. No API key or third-party package is required.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any

from weather_cli import config

WEATHER_CODES: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_json(url: str, timeout: int | None = None) -> dict[str, Any]:
    """Fetch and decode a JSON document.

    Args:
        url: Fully qualified URL to request.
        timeout: Seconds to wait; defaults to :data:`weather_cli.config.TIMEOUT`.

    Returns:
        The decoded top-level JSON object.

    Raises:
        OSError: If the request fails.
        ValueError: If the response is not valid JSON.
    """
    request = urllib.request.Request(url, headers={"User-Agent": config.USER_AGENT})
    effective_timeout = config.TIMEOUT if timeout is None else timeout
    with urllib.request.urlopen(request, timeout=effective_timeout) as response:
        data: dict[str, Any] = json.load(response)
    return data


def geocode(city: str) -> dict[str, Any]:
    """Return the first geocoding result for a city name.

    Args:
        city: Human-readable city name.

    Returns:
        The first result object containing at least latitude and longitude.

    Raises:
        ValueError: If the API returns no results.
    """
    params = urllib.parse.urlencode(
        {"name": city, "count": 1, "language": "en", "format": "json"}
    )
    data = get_json(f"{config.GEO_URL}?{params}")
    results: list[dict[str, Any]] = data.get("results") or []
    if not results:
        raise ValueError(f"City not found: {city!r}")
    result: dict[str, Any] = results[0]
    return result


def current_weather(
    latitude: float, longitude: float, unit: str | None = None
) -> dict[str, Any]:
    """Return the current-weather block for a coordinate.

    Args:
        latitude: Latitude in decimal degrees.
        longitude: Longitude in decimal degrees.
        unit: ``"celsius"`` or ``"fahrenheit"``; defaults to the configured unit.

    Returns:
        The ``current`` object from the forecast response.

    Raises:
        KeyError: If the API response has no ``current`` block.
    """
    effective_unit = config.DEFAULT_UNIT if unit is None else unit
    params: dict[str, Any] = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,relative_humidity_2m,apparent_temperature,"
            "weather_code,wind_speed_10m"
        ),
        "timezone": "auto",
    }
    if effective_unit == "fahrenheit":
        params["temperature_unit"] = "fahrenheit"
        params["wind_speed_unit"] = "mph"

    data = get_json(f"{config.FORECAST_URL}?{urllib.parse.urlencode(params)}")
    current: dict[str, Any] = data["current"]
    return current


def describe(code: int) -> str:
    """Translate a WMO weather code into a human-readable condition.

    Args:
        code: WMO weather code returned by Open-Meteo.

    Returns:
        A description, or ``"Unknown condition (code)"`` for unmapped codes.
    """
    return WEATHER_CODES.get(code, f"Unknown condition ({code})")


def format_report(place: dict[str, Any], current: dict[str, Any], unit: str) -> str:
    """Build the human-readable weather report.

    Args:
        place: Geocoding result with name, region and country fields.
        current: Current-weather fields from the forecast API.
        unit: ``"celsius"`` or ``"fahrenheit"``, controlling symbols and units.

    Returns:
        A multi-line report string.
    """
    symbol = "F" if unit == "fahrenheit" else "C"
    wind_unit = "mph" if unit == "fahrenheit" else "km/h"
    name = place.get("name", "Unknown")
    region = place.get("admin1")
    country = place.get("country")
    location = ", ".join(part for part in (name, region, country) if part)

    return "\n".join(
        [
            f"Weather for {location}",
            "-" * max(20, len(location) + 15),
            f"Condition   : {describe(current.get('weather_code', -1))}",
            f"Temperature : {current.get('temperature_2m')} °{symbol} "
            f"(feels like {current.get('apparent_temperature')} °{symbol})",
            f"Humidity    : {current.get('relative_humidity_2m')} %",
            f"Wind        : {current.get('wind_speed_10m')} {wind_unit}",
            f"Updated     : {current.get('time')}",
        ]
    )


__all__ = [
    "WEATHER_CODES",
    "current_weather",
    "describe",
    "format_report",
    "geocode",
    "get_json",
]
