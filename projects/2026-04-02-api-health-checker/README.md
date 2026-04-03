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