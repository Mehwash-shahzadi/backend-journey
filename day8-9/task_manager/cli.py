import click
from manager import TaskManager
from storage import save_to_file, load_from_file

TASKS_FILE = "tasks.json"

# Load tasks when CLI starts
manager = TaskManager()
try:
    load_from_file(TASKS_FILE, manager)
except Exception:
    pass  # If file not found or corrupted → start empty


@click.group()
def cli():
    """Simple CLI Task Manager"""
    pass


# add command
@cli.command()
@click.argument("title")
def add(title):
    """Add a new task"""
    task = manager.add(title)
    save_to_file(TASKS_FILE, manager)
    click.echo(f"Task added: {task.title} (id={task.id})")


# list command
@cli.command(name="list")
@click.option("--status", type=click.Choice(["pending", "completed"]), default=None)
@click.option("--sort", type=click.Choice(["asc", "desc"]), default="asc")
def list_tasks(status, sort):
    """List tasks with optional filtering and sorting"""

    tasks = manager.list()

    # Filtering
    if status:
        tasks = [t for t in tasks if t.status == status]

    # Sorting by creation date
    tasks.sort(key=lambda t: t.created_at, reverse=(sort == "desc"))

    if not tasks:
        click.echo("No tasks found.")
        return

    for task in tasks:
        click.echo(f"[{task.id}] {task.title} - {task.status} ({task.created_at})")



# complete command
@cli.command()
@click.argument("task_id", type=int)
def complete(task_id):
    """Mark a task as completed"""

    success = manager.complete(task_id)

    if success:
        save_to_file(TASKS_FILE, manager)
        click.echo(f"Task {task_id} marked as completed")
    else:
        click.echo("Error: Task not found")

# delete command
@cli.command()
@click.argument("task_id", type=int)
def delete(task_id):
    """Delete a task"""

    success = manager.delete(task_id)

    if success:
        save_to_file(TASKS_FILE, manager)
        click.echo(f"Task {task_id} deleted")
    else:
        click.echo("Error: Task not found")

