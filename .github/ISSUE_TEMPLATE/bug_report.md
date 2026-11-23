---
name: Bug report
about: Report a lookup, formatting or CLI problem
title: "[Bug]: "
labels: bug
assignees: ""
---

## What happened?

A clear and concise description of the problem.

## Expected behaviour

What you expected to happen instead.

## Steps to reproduce

1. Run `python -m weather_cli "<city>" [--unit ...]`.
2. Set `WEATHER_UNIT` / `WEATHER_TIMEOUT` if relevant.
3. Observe the problem.

## Environment

- OS and version:
- Python version (`python --version`):
- Repo commit / version:

## Output

Paste the exact command, output and traceback. The CLI prints API/network
errors on stderr with exit code 1. Please remove private network details.
