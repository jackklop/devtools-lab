import requests
import time

URLS = [
    "https://api.github.com",
    "https://jsonplaceholder.typicode.com/posts",
    "https://httpbin.org/status/200",
]

TIMEOUT_SECONDS = 5


def check_url(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
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
    results = []

    for url in URLS:
        results.append(check_url(url))

    print_results(results)


if __name__ == "__main__":
    main()