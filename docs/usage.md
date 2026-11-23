# Usage

Install the dev extras first (`pip install -r requirements-dev.txt`), or set
`PYTHONPATH=src` when running from a checkout.

## CLI reference

```text
usage: weather-cli [-h] [--unit {celsius,fahrenheit}] [--json] city

Get current weather for a city.

positional arguments:
  city                  city name, e.g. 'Patna' or 'New Delhi'

options:
  -h, --help            show this help message and exit
  --unit {celsius,fahrenheit}
                        temperature unit (default: celsius)
  --json                print raw JSON instead
```

### Default report

```bash
python -m weather_cli Patna
```

Real output:

```text
Weather for Patna, Bihar, India
----------------------------------
Condition   : Clear sky
Temperature : 19.3 °C (feels like 20.2 °C)
Humidity    : 78 %
Wind        : 5.6 km/h
Updated     : 2026-11-23T23:15
```

Values are live, so your output will differ.

### Fahrenheit

```bash
python -m weather_cli "New Delhi" --unit fahrenheit
```

Real output:

```text
Weather for New Delhi, National Capital Territory of Delhi, India
--------------------------------------------------------------------
Condition   : Clear sky
Temperature : 62.1 °F (feels like 61.4 °F)
Humidity    : 72 %
Wind        : 3.8 mph
Updated     : 2026-11-23T23:15
```

### Raw JSON

```bash
python -m weather_cli London --json
```

Real output (abridged only where marked):

```json
{
  "location": {
    "id": 2643743,
    "name": "London",
    "latitude": 51.50853,
    "longitude": -0.12574,
    "timezone": "Europe/London",
    "country": "United Kingdom",
    "admin1": "England"
  },
  "current": {
    "time": "2026-11-23T17:45",
    "interval": 900,
    "temperature_2m": 5.5,
    "relative_humidity_2m": 63,
    "apparent_temperature": 1.9,
    "weather_code": 0,
    "wind_speed_10m": 9.4
  }
}
```

The real response contains additional geocoding fields (`elevation`,
`feature_code`, IDs, population, `admin2`); they are omitted above for space.

### Errors

```console
$ python -m weather_cli NowherevilleXYZ; echo $?
error: City not found: 'NowherevilleXYZ'
1
```

## Environment configuration

| Variable | Default | Effect |
| --- | --- | --- |
| `WEATHER_UNIT` | `celsius` | Default for `--unit`; accepts `celsius` or `fahrenheit`. |
| `WEATHER_TIMEOUT` | `10` | HTTP timeout in seconds; positive integer. |

PowerShell:

```powershell
$env:WEATHER_UNIT = "fahrenheit"
$env:WEATHER_TIMEOUT = "5"
python -m weather_cli Patna          # fahrenheit report, 5s timeout
Remove-Item Env:WEATHER_UNIT, Env:WEATHER_TIMEOUT
```

POSIX shells:

```bash
WEATHER_UNIT=fahrenheit WEATHER_TIMEOUT=5 python -m weather_cli Patna
```

Unsupported units and non-positive/non-numeric timeouts are ignored and the
defaults are used. `--unit` always overrides `WEATHER_UNIT`.

## Public API

```python
from weather_cli import current_weather, format_report, geocode

place = geocode("Patna")
current = current_weather(place["latitude"], place["longitude"], "celsius")
print(format_report(place, current, "celsius"))
```

`describe(code)` maps a WMO code to text, and `get_json(url, timeout=None)` is
the single HTTP helper used by the library.

## Testing and linting

```bash
python -m unittest discover -s tests -v
python -m ruff check .
python -m mypy src/weather_cli
```
