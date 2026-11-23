"""Current-weather CLI built on the free Open-Meteo APIs, using only stdlib."""

from __future__ import annotations

from weather_cli.core.weather import current_weather, describe, format_report, geocode

__version__ = "1.1.0"

__all__ = ["current_weather", "describe", "format_report", "geocode", "__version__"]
