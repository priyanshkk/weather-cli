# Weather CLI

[![CI](https://github.com/priyanshkk/weather-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/priyanshkk/weather-cli/actions/workflows/tests.yml)
[![Linter](https://github.com/priyanshkk/weather-cli/actions/workflows/linter.yml/badge.svg)](https://github.com/priyanshkk/weather-cli/actions/workflows/linter.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Typing: mypy](https://img.shields.io/badge/typing-mypy-2f6fab.svg)](https://mypy.readthedocs.io/)
[![Tests: unittest](https://img.shields.io/badge/tests-unittest-green.svg)](https://docs.python.org/3/library/unittest.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Get current weather for any city from the terminal, with no API key.

## Overview / why

Weather lookups do not need a framework or an API key. This CLI uses the free
[Open-Meteo](https://open-meteo.com/) APIs through `urllib` from the standard
library. Requests, decoding, WMO code translation and formatting are separated
from the CLI layer, and all network access goes through one patchable function
so the tests never touch the internet.

## Tech stack

| Area | Choice | Why |
| --- | --- | --- |
| Language | Python 3.10–3.13 | Modern type syntax, no compiled runtime dependencies. |
| HTTP | `urllib.request`, `urllib.parse` | Standard library; no `requests` dependency. |
| Data | `json`, typed `dict[str, Any]` | Faithful to the API payloads. |
| API | Open-Meteo geocoding + forecast | Free, keyless, well documented. |
| Packaging | Hatchling, `src/` layout | Standard PEP 621 metadata and console script. |
| Tests / checks | unittest, Ruff, mypy (strict) | Offline suite plus static guarantees. |

## Real demo output

Live lookups performed from the CLI:

```console
$ python -m weather_cli Patna
Weather for Patna, Bihar, India
----------------------------------
Condition   : Clear sky
Temperature : 19.3 °C (feels like 20.2 °C)
Humidity    : 78 %
Wind        : 5.6 km/h
Updated     : 2026-11-23T23:15
```

```console
$ python -m weather_cli "New Delhi" --unit fahrenheit
Weather for New Delhi, National Capital Territory of Delhi, India
--------------------------------------------------------------------
Condition   : Clear sky
Temperature : 62.1 °F (feels like 61.4 °F)
Humidity    : 72 %
Wind        : 3.8 mph
Updated     : 2026-11-23T23:15
```

```console
$ python -m weather_cli NowherevilleXYZ; echo $?
error: City not found: 'NowherevilleXYZ'
1
```

Weather values are live and will differ when you run these commands.

## Install & setup

```bash
git clone https://github.com/priyanshkk/weather-cli.git
cd weather-cli
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Windows users can also run `powershell -File scripts\setup.ps1`; POSIX users can
run `bash scripts/setup.sh`. Runtime dependencies are stdlib only, so
`pip install -r requirements.txt` simply installs the package itself.

## Usage

```bash
python -m weather_cli Patna
python -m weather_cli "New Delhi" --unit fahrenheit
python -m weather_cli London --json
python weather.py Patna            # backward-compatible launcher
weather-cli Patna                  # installed console script
python -m weather_cli --help
```

Full examples, including the JSON shape and the public API, are in
[docs/usage.md](docs/usage.md).

## Project structure

```text
weather-cli/
├── .github/
│   ├── ISSUE_TEMPLATE/{bug_report,feature_request}.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/{tests,linter}.yml
├── docs/{index,architecture,usage}.md
├── scripts/{setup.ps1,setup.sh}
├── src/weather_cli/
│   ├── __init__.py
│   ├── __main__.py          # CLI parser and output
│   ├── config.py            # env-backed unit + timeout
│   └── core/
│       ├── __init__.py
│       └── weather.py       # HTTP, geocoding, formatting
├── tests/{__init__,test_core,test_main}.py
├── .env.example
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── weather.py               # compatibility shim
├── LICENSE
└── README.md
```

## Environment configuration

| Variable | Default | Meaning |
| --- | --- | --- |
| `WEATHER_UNIT` | `celsius` | Default unit; `celsius` or `fahrenheit`. `--unit` overrides it. |
| `WEATHER_TIMEOUT` | `10` | HTTP timeout in seconds (positive integer). |

Invalid values fall back to the defaults. See
[docs/architecture.md](docs/architecture.md) for where the values are applied.

## Testing & quality

```bash
python -m unittest discover -s tests -v
python -m ruff check .
python -m mypy src/weather_cli
python -m build
```

The suite runs on Python 3.10, 3.11, 3.12 and 3.13 in GitHub Actions and uses
mocked API responses, so it is offline and deterministic.

## Roadmap

- [ ] Optional daily forecast summary (`--forecast`).
- [ ] City lookup history stored locally.
- [ ] Configurable output template.
- [ ] Caching of geocoding results to reduce requests.

## License

MIT — see [LICENSE](LICENSE).
