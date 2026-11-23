"""Current-weather CLI built on the free Open-Meteo API.

No API key and no third-party packages: only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
USER_AGENT = "priyanshkk-weather-cli/1.0"

WEATHER_CODES = {
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


def get_json(url: str, timeout: int = 10) -> dict:
    """Fetch and decode JSON from *url*."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def geocode(city: str) -> dict:
    """Return the first geocoding result for *city*."""
    params = urllib.parse.urlencode(
        {"name": city, "count": 1, "language": "en", "format": "json"}
    )
    data = get_json(f"{GEO_URL}?{params}")
    results = data.get("results") or []
    if not results:
        raise ValueError(f"City not found: {city!r}")
    return results[0]


def current_weather(latitude: float, longitude: float, unit: str = "celsius") -> dict:
    """Return the current-weather block for a coordinate."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,relative_humidity_2m,apparent_temperature,"
            "weather_code,wind_speed_10m"
        ),
        "timezone": "auto",
    }
    if unit == "fahrenheit":
        params["temperature_unit"] = "fahrenheit"
        params["wind_speed_unit"] = "mph"

    data = get_json(f"{FORECAST_URL}?{urllib.parse.urlencode(params)}")
    return data["current"]


def describe(code: int) -> str:
    return WEATHER_CODES.get(code, f"Unknown condition ({code})")


def format_report(place: dict, current: dict, unit: str) -> str:
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Get current weather for a city.")
    parser.add_argument("city", help="city name, e.g. 'Patna' or 'New Delhi'")
    parser.add_argument(
        "--unit",
        choices=("celsius", "fahrenheit"),
        default="celsius",
        help="temperature unit (default: celsius)",
    )
    parser.add_argument("--json", action="store_true", help="print raw JSON instead")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        place = geocode(args.city)
        current = current_weather(place["latitude"], place["longitude"], args.unit)
    except (ValueError, KeyError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"location": place, "current": current}, indent=2))
    else:
        print(format_report(place, current, args.unit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
