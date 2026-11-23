"""Tests for the weather CLI entry point and environment configuration."""

from __future__ import annotations

import importlib
import io
import json
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from weather_cli import config  # noqa: E402
from weather_cli.__main__ import build_parser, main  # noqa: E402

ENV_KEYS = ("WEATHER_UNIT", "WEATHER_TIMEOUT")

PLACE = {
    "name": "Patna",
    "admin1": "Bihar",
    "country": "India",
    "latitude": 25.15,
    "longitude": 85.15,
}
CURRENT = {"temperature_2m": 30.5, "weather_code": 2, "time": "2026-11-23T10:00"}


class ParserTests(unittest.TestCase):
    """Cover CLI parsing and environment-driven defaults."""

    def test_default_city_and_unit(self) -> None:
        """The parser requires a city and defaults to the configured unit."""
        args = build_parser().parse_args(["Patna"])
        self.assertEqual(args.city, "Patna")
        self.assertEqual(args.unit, config.DEFAULT_UNIT)
        self.assertFalse(args.json)

    def test_explicit_unit_overrides_default(self) -> None:
        """--unit wins over the configured default."""
        args = build_parser().parse_args(["Patna", "--unit", "fahrenheit"])
        self.assertEqual(args.unit, "fahrenheit")

    def test_environment_sets_default_unit(self) -> None:
        """WEATHER_UNIT changes the parser default."""
        with patch.dict(os.environ, {"WEATHER_UNIT": "fahrenheit"}):
            importlib.reload(config)
            args = build_parser().parse_args(["Patna"])
        self.assertEqual(args.unit, "fahrenheit")

    def test_environment_sets_timeout(self) -> None:
        """WEATHER_TIMEOUT is read as a positive integer."""
        with patch.dict(os.environ, {"WEATHER_TIMEOUT": "3"}):
            importlib.reload(config)
            self.assertEqual(config.TIMEOUT, 3)

    def test_invalid_environment_falls_back(self) -> None:
        """Unsupported units and non-positive timeouts use defaults."""
        env = {"WEATHER_UNIT": "kelvin", "WEATHER_TIMEOUT": "0"}
        with patch.dict(os.environ, env):
            importlib.reload(config)
            self.assertEqual(config.DEFAULT_UNIT, "celsius")
            self.assertEqual(config.TIMEOUT, 10)

    def tearDown(self) -> None:
        """Restore config constants after each test."""
        for key in ENV_KEYS:
            os.environ.pop(key, None)
        importlib.reload(config)


class EntryPointTests(unittest.TestCase):
    """Cover success, error and JSON paths of main()."""

    def test_missing_city_returns_error_code(self) -> None:
        """A failed lookup prints to stderr and returns 1."""
        with (
            patch("weather_cli.__main__.geocode", side_effect=ValueError("not found")),
            redirect_stderr(io.StringIO()) as errors,
        ):
            result = main(["Nowhereville"])
        self.assertEqual(result, 1)
        self.assertIn("error: not found", errors.getvalue())

    def test_report_is_printed_on_success(self) -> None:
        """A successful lookup prints the formatted report."""
        with (
            patch("weather_cli.__main__.geocode", return_value=PLACE),
            patch("weather_cli.__main__.current_weather", return_value=CURRENT),
            redirect_stdout(io.StringIO()) as output,
        ):
            result = main(["Patna"])
        self.assertEqual(result, 0)
        self.assertIn("Weather for Patna, Bihar, India", output.getvalue())

    def test_json_flag_prints_parseable_json(self) -> None:
        """--json emits an object with location and current keys."""
        with (
            patch("weather_cli.__main__.geocode", return_value=PLACE),
            patch("weather_cli.__main__.current_weather", return_value=CURRENT),
            redirect_stdout(io.StringIO()) as output,
        ):
            result = main(["Patna", "--json"])
        self.assertEqual(result, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["location"]["name"], "Patna")
        self.assertEqual(payload["current"]["weather_code"], 2)


if __name__ == "__main__":
    unittest.main()
