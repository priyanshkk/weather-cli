$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)

python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt

Write-Host 'Setup complete. Activate with: .\.venv\Scripts\Activate.ps1'
Write-Host 'Then run: python -m weather_cli Patna'
