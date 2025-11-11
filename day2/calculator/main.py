"""Entry point for calculator demo with Rich formatting."""

from utils import add, subtract, multiply, divide, is_numeric
from rich import print 

if __name__ == "__main__":
    x, y = 10, 5

    if is_numeric(x) and is_numeric(y):
        print(f"[bold green]{x} + {y} = {add(x, y)}[/bold green]")
        print(f"[bold yellow]{x} - {y} = {subtract(x, y)}[/bold yellow]")
        print(f"[bold cyan]{x} * {y} = {multiply(x, y)}[/bold cyan]")
        print(f"[bold magenta]{x} / {y} = {divide(x, y)}[/bold magenta]")
    else:
        print("[bold red]Invalid input![/bold red]")
