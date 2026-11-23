#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-dev.txt

printf 'Setup complete. Activate with: source .venv/bin/activate\n'
printf 'Then run: python -m weather_cli Patna\n'
