import os
import random
from datetime import datetime

BASE_DIR = "projects"

PROJECT_TYPES = [
    "api-health-checker",
    "log-analyzer",
    "file-organizer"
]

def create_project():
    date_str = datetime.now().strftime("%Y-%m-%d")
    project_type = random.choice(PROJECT_TYPES)
    project_name = f"{date_str}-{project_type}"
    project_path = os.path.join(BASE_DIR, project_name)

    if os.path.exists(project_path):
        print("Project already exists today.")
        return

    os.makedirs(project_path)

    if project_type == "api-health-checker":
        create_api_checker(project_path)

    elif project_type == "log-analyzer":
        create_log_analyzer(project_path)

    elif project_type == "file-organizer":
        create_file_organizer(project_path)

    print("Created:", project_name)


# ---------------- PROJECT TYPES ---------------- #

def create_api_checker(path):
    main = """import requests

urls = ["https://api.github.com"]

for url in urls:
    try:
        res = requests.get(url)
        print(url, res.status_code)
    except Exception as e:
        print("Error:", e)
"""
    write_files(path, main, "requests\n", "API Health Checker tool")


def create_log_analyzer(path):
    main = """from collections import Counter

with open("sample.log", "r") as f:
    lines = f.readlines()

errors = [line for line in lines if "ERROR" in line]

print("Error count:", len(errors))
"""
    write_files(path, main, "", "Simple log analyzer tool")


def create_file_organizer(path):
    main = """import os
import shutil

source = "files"

for file in os.listdir(source):
    ext = file.split(".")[-1]
    os.makedirs(ext, exist_ok=True)
    shutil.move(os.path.join(source, file), os.path.join(ext, file))
"""
    write_files(path, main, "", "File organizer by extension")


# ---------------- HELPER ---------------- #

def write_files(path, main_code, requirements, description):
    readme = f"""# {description}

## Description
A useful utility tool.

## Usage
python main.py
"""

    with open(os.path.join(path, "main.py"), "w") as f:
        f.write(main_code)

    with open(os.path.join(path, "README.md"), "w") as f:
        f.write(readme)

    with open(os.path.join(path, "requirements.txt"), "w") as f:
        f.write(requirements)


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    create_project()