import sys
from rich import print
import requests
from typing import Union

def factorial(n: int) -> int:
    """Calculate the factorial of a number."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

if __name__ == "__main__":
    # Print Python version
    python_version = sys.version
    print(f"[bold green]Python Version:[/bold green] {python_version}")

    # Test factorial function
    number = 5
    fact_result = factorial(number)
    print(f"[bold cyan]Factorial of {number} is:[/bold cyan] {fact_result}")

    # Save output to file
    with open("output.txt", "w") as f:
        f.write(f"Python Version: {python_version}\n")
        f.write(f"Factorial of {number} is: {fact_result}\n")

    print("[bold yellow]Output saved to output.txt[/bold yellow]")