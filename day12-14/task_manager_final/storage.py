import json
from models import Task, Priority

def save_to_file(filename: str, manager) -> None:
    """Save manager.tasks to JSON file (Day 12)."""
    data = [t.to_dict() for t in manager.tasks]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_from_file(filename: str, manager) -> None:
    """Load tasks from JSON file into manager.tasks (Day 12)."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        # no existing data: leave manager.tasks empty
        return
    except json.JSONDecodeError:
        # corrupted file: skip loading
        return

    # populate manager.tasks
    manager.tasks = [Task.from_dict(item) for item in data]
