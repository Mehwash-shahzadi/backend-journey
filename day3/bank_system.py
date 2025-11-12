from rich import print
class BankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount<=0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        print(f"[bold green]Deposited:[/bold green] {amount}. [bold blue]New Balance:[/bold blue] {self.get_balance()}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
          print("[bold red]Withdrawal amount must be positive.[/bold red]")
          return
        if amount > self.balance:
          print("[bold red]Sorry! You don’t have enough balance to withdraw that amount.[/bold red]")
          return
        self.balance -= amount
        print(f"[bold red]Withdrew:[/bold red] {amount}. [bold blue]New Balance:[/bold blue] {self.get_balance()}")


    def get_balance(self) -> float:
        return self.balance
    
if __name__ == "__main__":
    print("[bold cyan]\n=== Welcome to the Bank System ===[/bold cyan]")

    account1 = BankAccount("Mishi", 1000.0)
    account2 = BankAccount("Ali", 500.0)
    account3 = BankAccount("Asif", 1200.0)

    # Account 1
    print(f"\n[bold yellow]--- Transactions for {account1.owner} ---[/bold yellow]")
    account1.deposit(500.0)
    account1.withdraw(200.0)
    account1.withdraw(1500.0)
    print(f"[bold blue]Final Balance:[/bold blue] {account1.get_balance()}")

    # Account 2
    print(f"\n[bold yellow]--- Transactions for {account2.owner} ---[/bold yellow]")
    account2.deposit(100.0)
    account2.withdraw(700.0)
    print(f"[bold blue]Final Balance:[/bold blue] {account2.get_balance()}")

    # Account 3
    print(f"\n[bold yellow]--- Transactions for {account3.owner} ---[/bold yellow]")
    account3.withdraw(300.0)
    print(f"[bold blue]Final Balance:[/bold blue] {account3.get_balance()}")

    print("[bold cyan]\n=== End of Transactions ===[/bold cyan]")
