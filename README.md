# Weather CLI

A command-line weather lookup tool built with **only the Python standard
library**. It uses the free [Open-Meteo](https://open-meteo.com/) APIs, so no
API key or sign-up is required.

## Usage

```bash
python weather.py Patna
python weather.py "New Delhi" --unit fahrenheit
python weather.py London --json
```

Example output:

```
Weather for Patna, Bihar, India
-------------------------------------
Condition   : Partly cloudy
Temperature : 30.5 °C (feels like 32.0 °C)
Humidity    : 60 %
Wind        : 12.3 km/h
Updated     : 2026-11-23T10:00
```

## How it works

1. `geocode()` resolves a city name to latitude/longitude using Open-Meteo's
   geocoding endpoint.
2. `current_weather()` fetches temperature, humidity, apparent temperature,
   WMO weather code and wind speed.
3. `format_report()` turns the raw data into a readable report, including a
   human-readable description for every WMO weather code.

All network access goes through `urllib.request`; `unittest.mock` patches the
single `get_json()` seam in the tests, so the suite never hits the network.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT
