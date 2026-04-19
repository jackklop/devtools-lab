# API Health Checker

A small Python utility that checks the health of public APIs by validating response status and measuring latency.

## Why I built this

This project is a lightweight backend utility for quickly checking whether important endpoints are reachable and responsive. It is useful as a starting point for uptime monitoring, alerting, and service diagnostics.

## Features

- Checks multiple API endpoints
- Measures response latency
- Handles timeouts and request failures
- Prints a simple pass/fail summary

## Tech Stack

- Python
- requests

## Project Structure

```text
api-health-checker/
├── main.py
├── requirements.txt
└── README.md
```

## Progress Log

- 2026-04-02: Add config file support
## Configuration
The tool now supports a `config.json` file for endpoints and timeout settings.

## Output
The script now exports health check results to `results.json`.

- 2026-04-02: Add JSON output
- 2026-04-03: Add retry logic
- 2026-04-04: Add CLI arguments
- 2026-04-06: Add logging to file
- 2026-04-07: Improve README with architecture section
- 2026-04-14: Add CSV export
- 2026-04-15: Add environment variable support
- 2026-04-18: Add simple tests
- 2026-04-19: Refactor health check logic into functions