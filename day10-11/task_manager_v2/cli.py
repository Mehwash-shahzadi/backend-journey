import click
from manager import TaskManager
from storage import save_to_file, load_from_file
from strategies import SortByDate, SortByPriority

TASKS_FILE = "tasks.json"

# Default sorter = SortByDate
manager = TaskManager(sorter=SortByDate())

try:
    load_from_file(TASKS_FILE, manager)
except:
    pass


@click.group()
def cli():
    """CLI Task Manager with Sorting Strategies"""
    pass


# ADD COMMAND
@cli.command()
@click.argument("title")
@click.option("--priority", type=int, default=1, help="Priority from 1-5")
def add(title, priority):
    task = manager.add(title, priority)
    save_to_file(TASKS_FILE, manager)
    click.echo(f" Added: {task}")


# LIST COMMAND
@cli.command(name="list")
def list_cmd():
    tasks = manager.list()

    if not tasks:
        click.echo("No tasks available.")
        return

    for task in tasks:
        click.echo(task)


# COMPLETE COMMAND
@cli.command()
@click.argument("task_id", type=int)
def complete(task_id):
    if manager.complete(task_id):
        save_to_file(TASKS_FILE, manager)
        click.echo(f"Task {task_id} completed")
    else:
        click.echo("Task not found")


# DELETE COMMAND
@cli.command()
@click.argument("task_id", type=int)
def delete(task_id):
    if manager.delete(task_id):
        save_to_file(TASKS_FILE, manager)
        click.echo(f"Task {task_id} deleted")
    else:
        click.echo("Task not found")
