import json
from pathlib import Path
from datetime import datetime


STATE_FILE = Path("project_state.json")


def load_state():
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def slugify(text: str) -> str:
    return (
        text.lower()
        .replace("add ", "")
        .replace("improve ", "")
        .replace("refactor ", "")
        .replace("polish ", "")
        .replace(" ", "-")
    )


def ensure_progress_section(readme_path: Path) -> str:
    if not readme_path.exists():
        return "# Project\n\n## Progress Log\n"

    content = readme_path.read_text(encoding="utf-8")
    if "## Progress Log" not in content:
        content += "\n## Progress Log\n"
    return content


def append_progress_log(project_path: Path, task: str):
    readme_path = project_path / "README.md"
    content = ensure_progress_section(readme_path)

    today = datetime.now().strftime("%Y-%m-%d")
    entry = f"\n- {today}: {task}"
    if entry not in content:
        content += entry

    readme_path.write_text(content, encoding="utf-8")


def apply_config_support(project_path: Path):
    config_path = project_path / "config.json"
    config_data = {
        "urls": [
            "https://api.github.com",
            "https://jsonplaceholder.typicode.com/posts",
            "https://httpbin.org/status/200"
        ],
        "timeout_seconds": 5
    }
    config_path.write_text(json.dumps(config_data, indent=2), encoding="utf-8")

    main_path = project_path / "main.py"
    if main_path.exists():
        main_code = """import json
import requests
import time
from pathlib import Path

CONFIG_PATH = Path("config.json")


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
    print("\\nAPI Health Check Results")
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


if __name__ == "__main__":
    main()
"""
        main_path.write_text(main_code, encoding="utf-8")


def apply_json_output(project_path: Path):
    main_path = project_path / "main.py"
    if not main_path.exists():
        return

    code = main_path.read_text(encoding="utf-8")
    if "results.json" in code:
        return

    code = code.replace(
        'def main():\n    config = load_config()\n    urls = config["urls"]\n    timeout_seconds = config.get("timeout_seconds", 5)\n\n    results = [check_url(url, timeout_seconds) for url in urls]\n    print_results(results)\n',
        '''def main():
    config = load_config()
    urls = config["urls"]
    timeout_seconds = config.get("timeout_seconds", 5)

    results = [check_url(url, timeout_seconds) for url in urls]
    print_results(results)

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
'''
    )

    main_path.write_text(code, encoding="utf-8")


def update_readme_for_task(project_path: Path, task: str):
    readme_path = project_path / "README.md"
    content = ensure_progress_section(readme_path)

    snippets = {
        "Add config file support": "\n## Configuration\nThe tool now supports a `config.json` file for endpoints and timeout settings.\n",
        "Add JSON output": "\n## Output\nThe script now exports health check results to `results.json`.\n",
    }

    snippet = snippets.get(task)
    if snippet and snippet not in content:
        content += snippet

    readme_path.write_text(content, encoding="utf-8")


def apply_task(project_path: Path, task: str):
    if task == "Add config file support":
        apply_config_support(project_path)
    elif task == "Add JSON output":
        apply_json_output(project_path)

    update_readme_for_task(project_path, task)
    append_progress_log(project_path, task)


def main():
    state = load_state()
    task_index = state["task_index"]
    tasks = state["tasks"]

    if task_index >= len(tasks):
        print("No remaining tasks.")
        return

    project_path = Path(state["current_project"])
    task = tasks[task_index]

    if not project_path.exists():
        raise FileNotFoundError(f"Project path not found: {project_path}")

    apply_task(project_path, task)

    state["last_task"] = task
    state["last_commit_message"] = slugify(task)
    state["task_index"] += 1
    save_state(state)

    print(f"Applied task: {task}")


if __name__ == "__main__":
    main()