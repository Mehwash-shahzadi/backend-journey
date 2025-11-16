from dataclasses import dataclass, field
from datetime import datetime
import json
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",#formate of the log messages
    filename="bank.log",
    filemode="a"
)

# Custom Exceptions
class NegativeAmountError(Exception):
    def __init__(self, amount):
        super().__init__(f"Amount must be positive. You entered: {amount}")

class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        super().__init__(f"Insufficient funds. Balance: {balance}, Withdrawal: {amount}")

# Transaction class
@dataclass
class Transaction:
    '''Class to represent a single transaction.'''
    amount: float
    type: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        '''Convert transaction to dictionary for JSON serialization.'''
        return {
            "amount": self.amount,
            "type": self.type,
            "timestamp": self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data):
        '''Create a Transaction object from a dictionary.'''
        return Transaction(
            amount=data["amount"],
            type=data["type"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )

# Transaction History
class TransactionHistory:
    def __init__(self):
        self.transactions: list[Transaction] = []

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def get_history(self, n=5):
        return self.transactions[-n:]

    def to_list(self):
        '''Convert transaction history to list of dictionaries for JSON serialization.'''
        return [t.to_dict() for t in self.transactions]

    @staticmethod
    def from_list(data_list):
        ''''deserialize a list of transaction dictionaries into a TransactionHistory object.'''
        transactionhistory = TransactionHistory()
        for d in data_list:
            transactionhistory.add_transaction(Transaction.from_dict(d))
        return transactionhistory

# BankAccount class
@dataclass
class BankAccount:
    owner: str
    balance: float = 0.0
    transaction_history: TransactionHistory = field(default_factory=TransactionHistory)

    # Deposit
    def deposit(self, amount: float):
        try:
            if amount <= 0:
                raise NegativeAmountError(amount)
            self.balance += amount
            t = Transaction(amount, "deposit")
            self.transaction_history.add_transaction(t)
            logging.info(f"{self.owner}: Deposited {amount}. Balance: {self.balance}")
        except NegativeAmountError as e:
            logging.error(str(e))
            raise

    # Withdraw
    def withdraw(self, amount: float):
        try:
            if amount <= 0:
                raise NegativeAmountError(amount)
            if amount > self.balance:
                raise InsufficientFundsError(self.balance, amount)
            self.balance -= amount
            t = Transaction(amount, "withdraw")
            self.transaction_history.add_transaction(t)
            logging.info(f"{self.owner}: Withdrew {amount}. Balance: {self.balance}")
        except (NegativeAmountError, InsufficientFundsError) as e:
            logging.error(str(e))
            raise

    # Print last 5 transactions
    def print_statement(self):
        print(f"\nAccount Statement for {self.owner}:")
        for t in self.transaction_history.get_history(5):
            print(f"{t.timestamp} - {t.type.upper()} - {t.amount}")
        print(f"Final Balance: {self.balance}\n")

    # Save to JSON file
    @staticmethod
    def save_to_file(accounts: dict, filename="bank_data.json"):
        try:
            data_to_save = {}
            for owner, acc in accounts.items():
                data_to_save[owner] = {
                    "balance": acc.balance,
                    "transactions": acc.transaction_history.to_list()
                }
            with open(filename, "w") as f:
                json.dump(data_to_save, f, indent=4)#indent mean to make the json file more readable
            logging.info("All accounts saved successfully.")
        except Exception as e:
            logging.error(f"Error saving accounts: {str(e)}")

    # Load from JSON file
    @staticmethod
    def load_from_file(filename="bank_data.json"):
        accounts = {}
        try:
            with open(filename, "r") as f:
                data_loaded = json.load(f)
            for owner, info in data_loaded.items():
                acc = BankAccount(owner, info["balance"])
                acc.transaction_history = TransactionHistory.from_list(info["transactions"])
                accounts[owner] = acc
            logging.info("All accounts loaded successfully.")
        except FileNotFoundError:
            logging.warning(f"{filename} not found. Starting with empty accounts.")
        except json.JSONDecodeError:
            logging.error(f"{filename} is corrupted. Starting with empty accounts.")
        return accounts

if __name__ == "__main__":
    accounts = {}

    # some accounts
    acc1 = BankAccount("Ali", 100)
    acc2 = BankAccount("Mishi", 500)
    accounts[acc1.owner] = acc1
    accounts[acc2.owner] = acc2

    # Transactions
    try:
        acc1.deposit(50)
        acc1.withdraw(30)
        acc2.deposit(200)
        acc2.withdraw(100)
    except Exception:
        pass

    # Print statements
    acc1.print_statement()
    acc2.print_statement()

    # Save to file
    BankAccount.save_to_file(accounts)

    # load data from file
    loaded_accounts = BankAccount.load_from_file()
    for acc in loaded_accounts.values():
        acc.print_statement()
