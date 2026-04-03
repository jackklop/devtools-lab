import json
from pathlib import Path
from datetime import datetime

STATE_FILE = Path("project_state.json")


def load_state():
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def update_readme(project_path: Path, task: str):
    readme_path = project_path / "README.md"

    if not readme_path.exists():
        readme_path.write_text("# Project\n\n", encoding="utf-8")

    content = readme_path.read_text(encoding="utf-8")

    if "## Progress Log" not in content:
        content += "\n## Progress Log\n"

    today = datetime.now().strftime("%Y-%m-%d")
    content += f"\n- {today}: {task}"

    readme_path.write_text(content, encoding="utf-8")


def main():
    state = load_state()

    task_index = state["task_index"]
    tasks = state["tasks"]

    if task_index >= len(tasks):
        print("No remaining tasks.")
        return

    project_path = Path(state["current_project"])
    task = tasks[task_index]

    update_readme(project_path, task)

    state["task_index"] += 1
    save_state(state)

    print(f"Applied task: {task}")


if __name__ == "__main__":
    main()