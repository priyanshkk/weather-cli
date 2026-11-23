"""Command-line entry point for the weather CLI.

Run with ``python -m weather_cli CITY`` or the installed ``weather-cli`` script.
"""

from __future__ import annotations

import argparse
import json
import sys

from weather_cli import config
from weather_cli.core.weather import current_weather, format_report, geocode


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser.

    Returns:
        A parser whose ``--unit`` default comes from ``WEATHER_UNIT``.
    """
    parser = argparse.ArgumentParser(
        prog="weather-cli", description="Get current weather for a city."
    )
    parser.add_argument("city", help="city name, e.g. 'Patna' or 'New Delhi'")
    parser.add_argument(
        "--unit",
        choices=config.VALID_UNITS,
        default=config.DEFAULT_UNIT,
        help=f"temperature unit (default: {config.DEFAULT_UNIT})",
    )
    parser.add_argument("--json", action="store_true", help="print raw JSON instead")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI.

    Args:
        argv: Optional argument list; defaults to ``sys.argv[1:]``.

    Returns:
        ``0`` on success, ``1`` when the lookup fails.
    """
    args = build_parser().parse_args(argv)
    try:
        place = geocode(args.city)
        current = current_weather(place["latitude"], place["longitude"], args.unit)
    except (ValueError, KeyError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"location": place, "current": current}, indent=2))
    else:
        print(format_report(place, current, args.unit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
