# Weather CLI documentation

A standard-library CLI that resolves a city with Open-Meteo and prints the
current weather. No API key and no third-party runtime packages.

- [Architecture](architecture.md) — modules, request flow and design decisions.
- [Usage](usage.md) — every command, environment variable and public API with
  real output.

Quick start:

```bash
pip install -r requirements-dev.txt
python -m weather_cli Patna
```
