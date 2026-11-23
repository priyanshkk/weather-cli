# Architecture

## Modules

| Module | Responsibility |
| --- | --- |
| `src/weather_cli/config.py` | API URLs, User-Agent, `WEATHER_UNIT` and `WEATHER_TIMEOUT` parsing. |
| `src/weather_cli/core/weather.py` | HTTP JSON fetch, geocoding, current-weather request, WMO code table, report formatting. |
| `src/weather_cli/__main__.py` | CLI parser, error handling and JSON/report output. |
| `src/weather_cli/__init__.py` | Public API re-exports and version. |
| `weather.py` | Thin compatibility shim for the original script name. |

## Request flow

```text
python -m weather_cli Patna --unit fahrenheit
        |
        v
__main__.main()
        |
        +-- geocode("Patna")
        |       `-- get_json(GEO_URL?name=Patna&count=1...) --> first result
        |
        +-- current_weather(lat, lon, "fahrenheit")
        |       `-- get_json(FORECAST_URL?...&temperature_unit=fahrenheit...)
        |
        `-- format_report(place, current, unit) --> stdout
            (or json.dumps({"location": ..., "current": ...}) with --json)
```

Both requests pass through `get_json()`, which builds the `urllib.request.Request`
with a stable User-Agent and applies the configured timeout. This is the only
place that opens a socket.

## Design decisions

1. **Standard library only.** `urllib.request`, `urllib.parse` and `json` cover
   the two GET requests. There is no runtime dependency to install or audit.
2. **One HTTP seam.** Tests patch `weather_cli.core.weather.get_json`, so the
   suite never uses the network. The timeout and User-Agent are applied inside
   `get_json()` where they cannot be forgotten by a new caller.
3. **Environment defaults with CLI override.** `WEATHER_UNIT` sets the parser
   default, and `--unit` overrides it per invocation. `WEATHER_TIMEOUT` is read
   once by `config.py`. Invalid values fall back to `celsius` and `10`.
4. **Fahrenheit changes wind units too.** Open-Meteo is asked for `mph` when
   Fahrenheit is selected; otherwise `km/h` is used. The report derives its
   labels from the same `unit` string, so symbols never disagree with data.
5. **WMO code mapping is data.** `WEATHER_CODES` is a plain dictionary in the
   core module. Unknown codes render as `Unknown condition (code)` instead of
   raising `KeyError`.
6. **Errors are exit codes.** `ValueError` (city not found), `KeyError` (bad
   API payload) and `OSError` (network/timeout) are caught in `main()`, printed
   to stderr as `error: ...`, and return exit code 1.

## Testing strategy

`tests/test_core.py` keeps the original logic tests and adds assertions for the
timeout/User-Agent seam. `tests/test_main.py` covers parser defaults, environment
variables, the report path, the `--json` path and the error path. Each test
module bootstraps `src/` into `sys.path`, so discovery works from the repository
root without an editable install.
