import json
import requests
import time
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"
RESULTS_PATH = Path(__file__).resolve().parent / "results.json"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def check_url(url, timeout_seconds):
    try:
        start = time.time()
        response = requests.get(url, timeout=timeout_seconds)
        latency_ms = round((time.time() - start) * 1000, 2)

        return {
            "url": url,
            "status": response.status_code,
            "latency_ms": latency_ms,
            "success": 200 <= response.status_code < 400,
            "error": None,
        }
    except requests.exceptions.Timeout:
        return {
            "url": url,
            "status": None,
            "latency_ms": None,
            "success": False,
            "error": "Request timed out",
        }
    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "status": None,
            "latency_ms": None,
            "success": False,
            "error": str(e),
        }


def print_results(results):
    print("\nAPI Health Check Results")
    print("-" * 60)

    success_count = 0
    for result in results:
        if result["success"]:
            success_count += 1
            print(
                f"PASS | {result['url']} | "
                f"status={result['status']} | "
                f"latency={result['latency_ms']} ms"
            )
        else:
            print(
                f"FAIL | {result['url']} | "
                f"status={result['status']} | "
                f"error={result['error']}"
            )

    print("-" * 60)
    print(f"Summary: {success_count}/{len(results)} checks passed")


def main():
    config = load_config()
    urls = config["urls"]
    timeout_seconds = config.get("timeout_seconds", 5)

    results = [check_url(url, timeout_seconds) for url in urls]
    print_results(results)

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
