import json
from models import Task
from datetime import datetime

def save_to_file(filename: str, manager):
    """Save all tasks from TaskManager to a JSON file"""
    tasks_dict = [task.to_dict() for task in manager.tasks]
    with open(filename, "w") as f:
        json.dump(tasks_dict, f, indent=4)


def load_from_file(filename: str, manager):
    """Load tasks from JSON file into TaskManager"""
    try:
        with open(filename, "r") as f:
            tasks_dict = json.load(f)
            manager.tasks = [Task.from_dict(d) for d in tasks_dict]
    except FileNotFoundError:
        manager.tasks = []
    except json.JSONDecodeError:
        manager.tasks = []
