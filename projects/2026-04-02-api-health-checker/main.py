import requests
import time

URLS = [
    "https://api.github.com",
    "https://jsonplaceholder.typicode.com/posts"
]

def check_health():
    for url in URLS:
        try:
            start = time.time()
            response = requests.get(url)
            latency = round((time.time() - start) * 1000, 2)

            print(f"{url} -> {response.status_code} ({latency} ms)")
        except Exception as e:
            print(f"{url} -> ERROR: {e}")

if __name__ == "__main__":
    check_health()
