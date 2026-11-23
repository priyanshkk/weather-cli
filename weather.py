"""Backward-compatible launcher for the weather CLI.

New code should use ``python -m weather_cli``. The ``src/`` path is bootstrapped
so this shim also works from a source checkout.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from weather_cli.__main__ import build_parser as build_parser  # noqa: E402
from weather_cli.__main__ import main as main  # noqa: E402
from weather_cli.core.weather import current_weather as current_weather  # noqa: E402
from weather_cli.core.weather import describe as describe  # noqa: E402
from weather_cli.core.weather import format_report as format_report  # noqa: E402
from weather_cli.core.weather import geocode as geocode  # noqa: E402
from weather_cli.core.weather import get_json as get_json  # noqa: E402

__all__ = [
    "build_parser",
    "current_weather",
    "describe",
    "format_report",
    "geocode",
    "get_json",
    "main",
]

if __name__ == "__main__":
    raise SystemExit(main())
