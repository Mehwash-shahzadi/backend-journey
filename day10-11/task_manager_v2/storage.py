import json
from models import Task


def save_to_file(filename, manager):
    '''Save tasks from the manager to a file'''
    tasks_dict = [task.to_dict() for task in manager.tasks]

    with open(filename, "w") as f:
        json.dump(tasks_dict, f, indent=4)


def load_from_file(filename, manager):
    '''Load tasks from a file into the manager'''
    with open(filename, "r") as f:
        tasks_list = json.load(f)

    for t in tasks_list:
        manager.tasks.append(Task.from_dict(t))
