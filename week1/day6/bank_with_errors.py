from dataclasses import dataclass, field
from datetime import datetime
import logging

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",#formate of the log messages
    filename="bank.log", 
    filemode="a"
)

# Custom Exceptions
class NegativeAmountError(Exception):
    """Raised when the amount is zero or negative."""
    def __init__(self, amount):
        super().__init__(f"Amount must be positive. You entered: {amount}")


class InsufficientFundsError(Exception):
    """Raised when withdrawal exceeds account balance."""
    def __init__(self, balance, amount):
        super().__init__(f"Insufficient funds. Balance: {balance}, Withdrawal: {amount}")


# Transaction Data Class
@dataclass
class Transaction:
    amount: float
    type: str  
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self):
        return f"{self.timestamp} - {self.type.upper()} - {self.amount}"

# TransactionHistory Class
class TransactionHistory:
    """Class to manage transaction history for a bank account."""
    def __init__(self):
        self.transactions: list[Transaction] = []

    def add_transaction(self, transaction: Transaction):
        """Add a new transaction to the history."""
        self.transactions.append(transaction)

    def get_history(self, n=5):
        """Get the last n transactions."""
        return self.transactions[-n:]

# Bank Account Base Class
@dataclass
class BankAccount:
    owner: str
    balance: float = 0.0
    transaction_history: TransactionHistory = field(default_factory=TransactionHistory)

    def deposit(self, amount: float):
        try:
            if amount <= 0:
                raise NegativeAmountError(amount)

            self.balance += amount
            transaction = Transaction(amount, "deposit")
            self.transaction_history.add_transaction(transaction)

            logging.info(f"{self.owner}: Deposited {amount}. Balance: {self.balance}")
            return self.balance

        except NegativeAmountError as e:
            logging.error(f"{self.owner}: {str(e)}")
            raise

    def withdraw(self, amount: float):
        try:
            if amount <= 0:
                raise NegativeAmountError(amount)

            if amount > self.balance:
                raise InsufficientFundsError(self.balance, amount)

            self.balance -= amount
            transaction = Transaction(amount, "withdraw")
            self.transaction_history.add_transaction(transaction)

            logging.info(f"{self.owner}: Withdrew {amount}. Balance: {self.balance}")
            return self.balance

        except (NegativeAmountError, InsufficientFundsError) as e:
            logging.error(f"{self.owner}: {str(e)}")
            raise

    def get_balance(self):
        return self.balance

    def print_statement(self):
        print(f"\nAccount Statement for {self.owner}:")
        for t in self.transaction_history.get_history(5):
            print(str(t))
        print(f"Final Balance: {self.balance}\n")

# Savings Account Class
class SavingsAccount(BankAccount):
    """Savings account with interest rate."""
    def __init__(self, owner: str, balance: float, interest_rate: float):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        """Apply interest to the account balance."""
        interest = self.balance * self.interest_rate / 100
        self.deposit(interest)
        logging.info(f"{self.owner}: Applied interest {interest}. New balance: {self.balance}")
        transaction = Transaction(interest, "interest")
        self.transaction_history.add_transaction(transaction)

# Checking Account Class
class CheckingAccount(BankAccount):
    """Checking account with overdraft limit."""
    def __init__(self, owner: str, balance: float, overdraft_limit: float):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float):
        try:
            if amount <= 0:
                raise NegativeAmountError(amount)

            if amount > self.balance + self.overdraft_limit:
                raise InsufficientFundsError(self.balance, amount)

            self.balance -= amount
            transaction = Transaction(amount, "withdraw")
            self.transaction_history.add_transaction(transaction)

            logging.info(f"{self.owner}: Withdrew {amount}. Balance: {self.balance}")
            return self.balance

        except (NegativeAmountError, InsufficientFundsError) as e:
            logging.error(f"{self.owner}: {str(e)}")
            raise

# Account Manager Class 
class AccountManager:
    """Manage bank accounts."""
    def __init__(self):
        self.accounts = {}

    def create_account(self, owner: str, balance: float = 0.0) -> BankAccount:
        if owner in self.accounts:
            raise ValueError(f"Account for {owner} already exists.")
        account = BankAccount(owner, balance)
        self.accounts[owner] = account
        return account

    def get_account(self, owner: str) -> BankAccount:
        if owner not in self.accounts:
            raise ValueError(f"Account for {owner} does not exist.")
        return self.accounts[owner]

if __name__ == "__main__":
    acc1 = BankAccount("Ali", 100)
    acc2 = SavingsAccount("Mishi", 500, 2.0)
    acc3 = CheckingAccount("Saima", 200, 100)

    # Invalid deposit
    # try:
    #     acc1.deposit(-50)
    # except Exception:
    #     pass

    # Insufficient funds withdraw
    # try:
    #     acc1.withdraw(200)
    # except Exception:
    #     pass

    # Apply interest
    # acc2.apply_interest()

    #Valid operations
    acc1.deposit(150)
    acc1.withdraw(50)

    # acc2.deposit(100)
    # acc3.withdraw(250)

    # Print statements
    acc1.print_statement()
    # acc2.print_statement()
    # acc3.print_statement()
