import click
from rich.console import Console
from rich.table import Table
from models import Priority
from manager import TaskManager
from strategies import SortByDate, SortByPriority
from storage import save_to_file, load_from_file

TASKS_FILE = "tasks.json"
console = Console()#console object for rich output

# Default manager uses SortByDate strategy
manager = TaskManager(sorter=SortByDate())
# Load existing tasks if any
load_from_file(TASKS_FILE, manager)


#cli group
@click.group()
def cli():
    """Task Manager CLI."""
    pass

# Add command
@cli.command()
@click.argument("title")
@click.option("--priority", type=click.Choice(["HIGH", "MEDIUM", "LOW"]), default="MEDIUM",
              help="Priority level")
@click.option("--tags", default="", help="Comma-separated tags, e.g. work,home")
def add(title, priority, tags):
    """Add a new task with optional priority and tags (Day 12)."""
    pr = Priority(priority)#convert string to Priority enum
    tags_list = [t.strip() for t in tags.split(",")] if tags else []
    task = manager.add(title, priority=pr, tags=tags_list)
    save_to_file(TASKS_FILE, manager)
    console.print(f"[green]Task added[/green] {task}")

#filtered list command
@cli.command(name="list")
@click.option("--status", type=click.Choice(["pending", "completed"]), default=None, help="Filter by status")
@click.option("--priority", type=click.Choice(["HIGH", "MEDIUM", "LOW"]), default=None, help="Filter by priority")
@click.option("--tag", default=None, help="Filter by tag")
@click.option("--sort", type=click.Choice(["date", "priority"]), default="date", help="Sort by date or priority")
@click.option("--desc", is_flag=True, help="Reverse order")
def list_cmd(status, priority, tag, sort, desc):
    # choose sorter strategy based on --sort
    if sort == "priority":
        manager.sorter = SortByPriority()
    else:
        manager.sorter = SortByDate()

    pr_enum = Priority(priority) if priority else None
    tasks = manager.list(status=status, priority=pr_enum, tag=tag, sort_desc=desc)

    if not tasks:
        console.print("[yellow]No tasks found[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Title")
    table.add_column("Status")
    table.add_column("Priority")
    table.add_column("Tags")
    table.add_column("Created At")

    for t in tasks:
        pri_color = "green" if t.priority == Priority.LOW else ("yellow" if t.priority == Priority.MEDIUM else "red")
        table.add_row(str(t.id), t.title, t.status, f"[{pri_color}]{t.priority.value}[/{pri_color}]",
                      ", ".join(t.tags), t.created_at.strftime("%Y-%m-%d %H:%M"))

    console.print(table)

#export command
@cli.command()
@click.option("--filename", default="tasks_export.csv", help="CSV file name")
def export(filename):
    """Export tasks to CSV."""
    manager.export_to_csv(filename)
    console.print(f"[green]Exported to[/green] {filename}")

#stats command
@cli.command()
@click.option("--overdue-days", default=7, help="Days after which a pending task is overdue (Day 13)")
def stats(overdue_days):
    """Show task statistics."""
    stat = manager.statistics(overdue_days=overdue_days)
    table = Table(show_header=False)
    table.add_row("Total tasks:", str(stat["total"]))
    table.add_row("Completed:", f"{stat['completed']} ({stat['completed_pct']}%)")
    table.add_row("Overdue:", str(stat["overdue"]))
    console.print(table)


#complete command
@cli.command()
@click.argument("task_id", type=int)
def complete(task_id):
    """Mark a task as completed."""
    if manager.complete(task_id):
        save_to_file(TASKS_FILE, manager)
        console.print(f"[green]Task {task_id} marked completed[/green]")
    else:
        console.print(f"[red]Task {task_id} not found[/red]")

#delete command
@cli.command()
@click.argument("task_id", type=int)
def delete(task_id):
    """Delete a task."""
    if manager.delete(task_id):
        save_to_file(TASKS_FILE, manager)
        console.print(f"[green]Task {task_id} deleted[/green]")
    else:
        console.print(f" [red]Task {task_id} not found[/red]")
