"""Unit tests for weather lookup, decoding and formatting."""

from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from weather_cli import config  # noqa: E402
from weather_cli.core.weather import (  # noqa: E402
    current_weather,
    describe,
    format_report,
    geocode,
    get_json,
)

PLACE = {"name": "Patna", "admin1": "Bihar", "country": "India"}
CURRENT = {
    "temperature_2m": 30.5,
    "apparent_temperature": 32.0,
    "relative_humidity_2m": 60,
    "weather_code": 2,
    "wind_speed_10m": 12.3,
    "time": "2026-11-23T10:00",
}


class WeatherCoreTests(unittest.TestCase):
    """Cover the original logic plus the HTTP seam."""

    def test_describe_known_and_unknown_codes(self) -> None:
        """Mapped WMO codes have names; others get an explicit fallback."""
        self.assertEqual(describe(0), "Clear sky")
        self.assertEqual(describe(95), "Thunderstorm")
        self.assertIn("Unknown", describe(999))

    def test_geocode_returns_first_result(self) -> None:
        """Geocoding picks the first result and encodes the city in the URL."""
        payload = {
            "results": [
                {"name": "Patna", "country": "India", "latitude": 25.15, "longitude": 85.15},
                {"name": "Patna City", "country": "India"},
            ]
        }
        with patch("weather_cli.core.weather.get_json", return_value=payload) as fetch:
            result = geocode("Patna")
        self.assertEqual(result["name"], "Patna")
        self.assertIn("name=Patna", fetch.call_args.args[0])

    def test_geocode_raises_for_unknown_city(self) -> None:
        """An empty result list is reported as a ValueError."""
        with (
            patch("weather_cli.core.weather.get_json", return_value={"results": []}),
            self.assertRaises(ValueError),
        ):
            geocode("Nowhereville")

    def test_current_weather_defaults_to_configured_unit(self) -> None:
        """With no unit argument the WEATHER_UNIT default is used."""
        payload = {"current": CURRENT}
        with patch("weather_cli.core.weather.get_json", return_value=payload) as fetch:
            result = current_weather(25.1, 85.1)
        self.assertEqual(result, CURRENT)
        url = fetch.call_args.args[0]
        self.assertNotIn("temperature_unit=fahrenheit", url)

    def test_current_weather_switches_units(self) -> None:
        """Fahrenheit requests also switch wind speed to mph."""
        payload = {"current": CURRENT}
        with patch("weather_cli.core.weather.get_json", return_value=payload) as fetch:
            result = current_weather(25.1, 85.1, "fahrenheit")
        self.assertEqual(result, CURRENT)
        url = fetch.call_args.args[0]
        self.assertIn("temperature_unit=fahrenheit", url)
        self.assertIn("wind_speed_unit=mph", url)

    def test_get_json_uses_configured_timeout_and_user_agent(self) -> None:
        """The single HTTP seam sends the configured timeout and User-Agent."""
        with patch("weather_cli.core.weather.urllib.request.urlopen") as opener:
            opener.return_value.__enter__.return_value = io.StringIO('{"ok": true}')
            data = get_json("https://example.test/data")
        self.assertEqual(data, {"ok": True})
        self.assertEqual(opener.call_args.kwargs["timeout"], config.TIMEOUT)
        request = opener.call_args.args[0]
        self.assertEqual(request.get_header("User-agent"), config.USER_AGENT)

    def test_format_report_contains_key_fields(self) -> None:
        """The report shows location, condition, temperature, wind and time."""
        report = format_report(PLACE, CURRENT, "celsius")
        self.assertIn("Patna, Bihar, India", report)
        self.assertIn("Partly cloudy", report)
        self.assertIn("30.5 °C", report)
        self.assertIn("12.3 km/h", report)
        self.assertIn("2026-11-23T10:00", report)

    def test_format_report_fahrenheit_units(self) -> None:
        """Fahrenheit reports use F and mph."""
        report = format_report(PLACE, CURRENT, "fahrenheit")
        self.assertIn("30.5 °F", report)
        self.assertIn("12.3 mph", report)


if __name__ == "__main__":
    unittest.main()
