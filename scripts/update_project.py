import os
from datetime import datetime

BASE_DIR = "projects"

def create_project():
    date_str = datetime.now().strftime("%Y-%m-%d")
    project_name = f"{date_str}-api-health-checker"
    project_path = os.path.join(BASE_DIR, project_name)

    if os.path.exists(project_path):
        print("Project already exists for today.")
        return

    os.makedirs(project_path)

    # main.py
    main_code = """import requests
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
"""

    # README (no fancy formatting to avoid errors)
    readme = """# API Health Checker

A simple tool to monitor API availability and latency.

## Features
- Checks HTTP status codes
- Measures response latency

## How to run
pip install -r requirements.txt
python main.py
"""

    # requirements.txt
    requirements = "requests\n"

    # write files
    with open(os.path.join(project_path, "main.py"), "w") as f:
        f.write(main_code)

    with open(os.path.join(project_path, "README.md"), "w") as f:
        f.write(readme)

    with open(os.path.join(project_path, "requirements.txt"), "w") as f:
        f.write(requirements)

    print("Project created:", project_name)


if __name__ == "__main__":
    create_project()