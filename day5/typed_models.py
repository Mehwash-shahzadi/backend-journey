from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class Transaction:
    """Class to represent a single transaction."""
    id: int
    type: str
    amount: float
    balance_after: float
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.type}: {self.amount}, Balance after: {self.balance_after}"


@dataclass
class TransactionHistory:
    """Class to manage transaction history for a bank account."""
    transactions: List[Transaction] = field(default_factory=list)

    def add_transaction(self, transaction: Transaction) -> None:
        """Adds a new transaction to the history."""
        self.transactions.append(transaction)

    def get_history(self, n: int = 5) -> List[Transaction]:
        """Returns the last `n` transactions."""
        return self.transactions[-n:]


@dataclass
class BankAccount:
    """Basic bank account with deposit and withdrawal functionalities."""
    owner: str
    balance: float
    transaction_history: TransactionHistory = field(default_factory=TransactionHistory)

    def deposit(self, amount: float) -> None:
        """Deposits money into the account and records the transaction."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        print(f"[bold green]Deposited:[/bold green] {amount}. [bold blue]New Balance:[/bold blue] {self.get_balance()}")
        self.transaction_history.add_transaction(Transaction(id=len(self.transaction_history.transactions)+1, type="Deposit", amount=amount, balance_after=self.balance))

    def withdraw(self, amount: float) -> None:
        """Withdraws money from the account and records the transaction."""
        if amount <= 0:
            print("[bold red]Withdrawal amount must be positive.[/bold red]")
            return
        if amount > self.balance:
            print("[bold red]Sorry! You don’t have enough balance to withdraw that amount.[/bold red]")
            return
        self.balance -= amount
        print(f"[bold red]Withdrew:[/bold red] {amount}. [bold blue]New Balance:[/bold blue] {self.get_balance()}")
        self.transaction_history.add_transaction(Transaction(id=len(self.transaction_history.transactions)+1, type="Withdrawal", amount=amount, balance_after=self.balance))

    def get_balance(self) -> float:
        """Returns the current balance of the account."""
        return self.balance


# Subclasses
@dataclass
class SavingsAccount(BankAccount):
    """Savings account with interest rate."""
    interest_rate: float

    def apply_interest(self) -> None:
        """Applies interest to the account balance."""
        interest = self.balance * self.interest_rate / 100
        self.deposit(interest)
        print(f"[bold magenta]Applied Interest:[/bold magenta] {interest}. [bold blue]New Balance:[/bold blue] {self.get_balance()}")
        self.transaction_history.add_transaction(Transaction(id=len(self.transaction_history.transactions)+1, type="Interest", amount=interest, balance_after=self.balance))


@dataclass
class CheckingAccount(BankAccount):
    """Checking account with overdraft limit."""
    overdraft_limit: float

    def withdraw(self, amount: float) -> None:
        """Withdraws money, considering the overdraft limit."""
        if amount <= 0:
            print("[bold red]Withdrawal amount must be positive.[/bold red]")
            return
        if amount > self.balance + self.overdraft_limit:
            print("[bold red]Sorry! You don’t have enough balance to withdraw that amount including overdraft limit.[/bold red]")
            return
        self.balance -= amount
        print(f"[bold red]Withdrew:[/bold red] {amount}. [bold blue]New Balance:[/bold blue] {self.get_balance()}")
        self.transaction_history.add_transaction(Transaction(id=len(self.transaction_history.transactions)+1, type="Withdrawal", amount=amount, balance_after=self.balance))


@dataclass
class AccountManager:
    """Manage accounts."""
    accounts: List[BankAccount] = field(default_factory=list)

    def create_account(self, owner: str, account_type: str, balance: float, **kwargs) -> BankAccount:
        """Creates and returns a new account."""
        if account_type == "savings":
            account = SavingsAccount(owner=owner, balance=balance, **kwargs)
        elif account_type == "checking":
            account = CheckingAccount(owner=owner, balance=balance, **kwargs)
        else:
            raise ValueError(f"Unknown account type: {account_type}")
        self.accounts.append(account)
        return account


if __name__ == "__main__":
    print("[bold cyan]\n=== Welcome to the Bank System v2 ===[/bold cyan]")

    # Create an Account Manager instance
    manager = AccountManager()

    # Create a Savings Account
    savings = manager.create_account(owner="Mishi", account_type="savings", balance=1000.0, interest_rate=0.02)
    print(f"\n[bold yellow]--- {savings.owner}'s Savings Account ---[/bold yellow]")
    savings.deposit(200)
    savings.apply_interest()
    print(f"[bold blue]Final Balance:[/bold blue] {savings.get_balance()}")
    print("[bold magenta]Last transactions:[/bold magenta]", savings.transaction_history.get_history(3))

    # Create a Checking Account
    checking = manager.create_account(owner="Ali", account_type="checking", balance=100.0, overdraft_limit=200.0)
    print(f"\n[bold yellow]--- {checking.owner}'s Checking Account ---[/bold yellow]")
    checking.withdraw(250)
    checking.withdraw(100)
    print(f"[bold blue]Final Balance:[/bold blue] {checking.get_balance()}")
    print("[bold magenta]Last transactions:[/bold magenta]", checking.transaction_history.get_history(3))

    print("[bold cyan]\n=== End of Transactions ===[/bold cyan]")
