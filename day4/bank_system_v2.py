from rich import print
from typing import List
from datetime import datetime

class Transaction:
    """Class to represent a single transaction."""
    def __init__(self,type:str,amount:float,balance_after:float,date_time:datetime):
        self.type = type
        self.amount = amount
        self.balance_after = balance_after
        self.timestamp = datetime.now()

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.type}: {self.amount}, Balance after: {self.balance_after}"

class TransactionHistory:
    """Class to manage transaction history for a bank account."""
    def __init__(self):
        self.transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        """Adds a new transaction to the history."""
        self.transactions.append(transaction)

    def get_history(self,n=5) -> List[Transaction]:
        """Returns the last `n` transactions."""
        return self.transactions[-n:]


class BankAccount:
    '''Basic bank account with deposit and withdrawal functionalities.'''
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.balance = balance
        self.transaction_history = TransactionHistory() # composition

    def deposit(self, amount: float) -> None:
        """Deposits money into the account and records the transaction."""
        if amount<=0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        print(f"[bold green]Deposited:[/bold green] {amount}. [bold blue]New Balance:[/bold blue] {self.get_balance()}")
        self.transaction_history.add_transaction(Transaction("Deposit",amount,self.balance,datetime.now()))

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
        self.transaction_history.add_transaction(Transaction("Withdrawal",amount,self.balance,datetime.now()))


    def get_balance(self) -> float:
        """Returns the current balance of the account."""
        return self.balance
    
#subclasses
class SavingsAccount(BankAccount):
    '''savings account with interest rate'''
    
    def __init__(self, owner: str, balance: float, interest_rate: float):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def apply_interest(self) -> None:
        """Applies interest to the account balance."""
        interest = self.balance * self.interest_rate / 100
        self.deposit(interest)
        print(f"[bold magenta]Applied Interest:[/bold magenta] {interest}. [bold blue]New Balance:[/bold blue] {self.get_balance()}")
        self.transaction_history.add_transaction(Transaction("Interest",interest,self.balance,datetime.now()))

class CheckingAccount(BankAccount):
    '''checking account with overdraft limit'''
    def __init__(self, owner: str, balance: float, overdraft_limit: float):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

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
        self.transaction_history.add_transaction(Transaction("Withdrawal",amount,self.balance,datetime.now()))

if __name__ == "__main__":
    print("[bold cyan]\n=== Welcome to the Bank System v2 ===[/bold cyan]")

    # Savings Account
    savings = SavingsAccount("Mishi", 1000.0, interest_rate=0.02)
    print(f"\n[bold yellow]--- {savings.owner}'s Savings Account ---[/bold yellow]")
    savings.deposit(200)
    savings.apply_interest()
    print(f"[bold blue]Final Balance:[/bold blue] {savings.get_balance()}")
    print("[bold magenta]Last transactions:[/bold magenta]", savings.transaction_history.get_history(3))


    # Checking Account
    checking = CheckingAccount("Ali", 100.0, overdraft_limit=200.0)
    print(f"\n[bold yellow]--- {checking.owner}'s Checking Account ---[/bold yellow]")
    checking.withdraw(250)
    checking.withdraw(100)
    print(f"[bold blue]Final Balance:[/bold blue] {checking.get_balance()}")
    print("[bold magenta]Last transactions:[/bold magenta]", checking.transaction_history.get_history(3))

    print("[bold cyan]\n=== End of Transactions ===[/bold cyan]")


#  Design Notes:
# Inheritance → used so SavingsAccount & CheckingAccount can reuse
# common deposit/withdraw logic from BankAccount.
# Composition → each account "has-a" TransactionHistory to track actions.