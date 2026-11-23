import unittest
from unittest.mock import patch

import weather


class WeatherTests(unittest.TestCase):
    def test_describe_known_and_unknown_codes(self):
        self.assertEqual(weather.describe(0), "Clear sky")
        self.assertEqual(weather.describe(95), "Thunderstorm")
        self.assertIn("Unknown", weather.describe(999))

    def test_geocode_returns_first_result(self):
        payload = {
            "results": [
                {"name": "Patna", "country": "India", "latitude": 25.15, "longitude": 85.15},
                {"name": "Patna City", "country": "India"},
            ]
        }
        with patch.object(weather, "get_json", return_value=payload) as fetch:
            result = weather.geocode("Patna")
        self.assertEqual(result["name"], "Patna")
        self.assertIn("name=Patna", fetch.call_args.args[0])

    def test_geocode_raises_for_unknown_city(self):
        with patch.object(weather, "get_json", return_value={"results": []}):
            with self.assertRaises(ValueError):
                weather.geocode("Nowhereville")

    def test_current_weather_switches_units(self):
        payload = {"current": {"temperature_2m": 70, "weather_code": 1}}
        with patch.object(weather, "get_json", return_value=payload) as fetch:
            result = weather.current_weather(25.1, 85.1, "fahrenheit")
        self.assertEqual(result, payload["current"])
        self.assertIn("temperature_unit=fahrenheit", fetch.call_args.args[0])

    def test_format_report_contains_key_fields(self):
        place = {"name": "Patna", "admin1": "Bihar", "country": "India"}
        current = {
            "temperature_2m": 30.5,
            "apparent_temperature": 32.0,
            "relative_humidity_2m": 60,
            "weather_code": 2,
            "wind_speed_10m": 12.3,
            "time": "2026-11-23T10:00",
        }
        report = weather.format_report(place, current, "celsius")
        self.assertIn("Patna, Bihar, India", report)
        self.assertIn("Partly cloudy", report)
        self.assertIn("30.5 °C", report)
        self.assertIn("12.3 km/h", report)

    def test_main_returns_error_code_for_missing_city(self):
        with patch.object(weather, "get_json", return_value={"results": []}):
            self.assertEqual(weather.main(["Nowhereville"]), 1)


if __name__ == "__main__":
    unittest.main()
