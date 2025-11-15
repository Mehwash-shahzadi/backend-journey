# 90-Day Backend Engineering Journey

## Why This Challenge?

I've been dabbling with Python for a while, but never had the structure to become job-ready. So I'm committing to 90 days - 2 hours daily, building real projects instead of following tutorials.

**Goal:** Go from writing scripts to building production-grade backend applications. By day 90, I want to confidently apply for backend developer roles.

This repo is my public accountability. Week 1 complete (Days 1-7). Let's see where this goes.

## Quick Start

```bash
git clone https://github.com/your-username/backend-journey.git
cd backend-journey
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Progress

### Week 1: Python Foundations

#### Day 1: Environment Setup

**What I Built:** Setup verification script with factorial calculation and file I/O

Focused on getting the environment right - virtual environments, type hints, and the Rich library for better terminal output. Wrote a simple script that checks Python version and writes results to a file.

```bash
python day01/setup_check.py
```

**Key Takeaways:**

- Virtual environments keep dependencies clean
- Type hints make code more readable
- Rich library makes terminal output actually look good

---

### Day 2: Modules & Packages

**What I Built:** Multi-file calculator with custom utility modules

Created a calculator that's split across multiple files. The `utils/` package has separate modules for math operations and input validation. This was my first time organizing code into a proper package structure.

```bash
python day02/calculator/main.py
```

**Key Takeaways:**

- `__init__.py` makes a folder into a package
- Separating concerns makes code easier to maintain
- Importing from custom modules isn't that scary

---

### Day 3: OOP Basics

**What I Built:** Basic banking system with BankAccount class

Built my first real class - a BankAccount with deposit and withdrawal methods. Added validation to prevent negative deposits and overdrafts. Used Rich for colored console output.

```python
class BankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
```

```bash
python day03/bank_system.py
```

**Key Takeaways:**

- Classes bundle data and behavior together
- Validation in methods prevents bad state
- Exception handling is important

---

### Day 4: Inheritance & Composition

**What I Built:** Extended banking system with account types and transaction history

Added SavingsAccount and CheckingAccount using inheritance. Implemented TransactionHistory using composition - each account now tracks its transactions. This is where OOP concepts finally clicked.

```python
class SavingsAccount(BankAccount):
    def __init__(self, owner: str, balance: float, interest_rate: float):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def apply_interest(self) -> None:
        interest = self.balance * self.interest_rate / 100
        self.deposit(interest)
```

```bash
python day04/bank_system_v2.py
```

**Key Takeaways:**

- Inheritance lets you extend base classes
- Composition (has-a) is often better than inheritance (is-a)
- `super()` calls parent class methods

---

### Day 5: Dataclasses & Type Hints

**What I Built:** Rewrote the entire banking system using dataclasses and proper type hints

Converted all my classes from Day 4 to use Python's `@dataclass` decorator. Added complete type annotations to every function and method. Ran `mypy` for the first time to catch type errors - found a few bugs I didn't know existed!

```python
@dataclass
class Transaction:
    id: int
    type: str
    amount: float
    balance_after: float
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class BankAccount:
    owner: str
    balance: float
    transaction_history: TransactionHistory = field(default_factory=TransactionHistory)

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
```

```bash
python day05/typed_models.py
# Check types with mypy
mypy day05/typed_models.py
```

**Key Takeaways:**

- Dataclasses auto-generate `__init__`, `__repr__`, and `__eq__` methods
- Type hints make code self-documenting and catch bugs early
- `mypy` is like a spell-checker for your types
- `field(default_factory=list)` prevents mutable default arguments bug

---

### Day 6: Exception Handling & Logging

**What I Built:** Added proper error handling and logging to the banking system

Replaced all those print statements with a proper logging system. Created custom exceptions for specific error cases like insufficient funds and negative amounts. Now when something goes wrong, I know exactly what happened and when - everything gets logged to `bank.log`.

```python
# Custom Exceptions
class NegativeAmountError(Exception):
    """Raised when the amount is zero or negative."""
    def __init__(self, amount):
        super().__init__(f"Amount must be positive. You entered: {amount}")

class InsufficientFundsError(Exception):
    """Raised when withdrawal exceeds account balance."""
    def __init__(self, balance, amount):
        super().__init__(f"Insufficient funds. Balance: {balance}, Withdrawal: {amount}")

# Using them in BankAccount
def withdraw(self, amount: float):
    try:
        if amount <= 0:
            raise NegativeAmountError(amount)
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)

        self.balance -= amount
        logging.info(f"{self.owner}: Withdrew {amount}. Balance: {self.balance}")

    except (NegativeAmountError, InsufficientFundsError) as e:
        logging.error(f"{self.owner}: {str(e)}")
        raise
```

```bash
python day06/bank_with_errors.py
# Check the generated log file
cat bank.log
```

**What I Learned:**

_Try/Except Blocks:_ Think of it like a safety net - you "try" risky code, and if it fails, you "catch" the error instead of crashing. Like catching a ball before it hits the ground.

_Custom Exceptions:_ Instead of generic errors, you create specific ones (like `InsufficientFundsError`). It's like having different alarm sounds - you instantly know what went wrong.

_Logging:_ Better than print statements because it saves everything to a file with timestamps. You can track what happened even after the program closes - super useful for debugging production issues.

**Key Takeaways:**

- Never let your program crash silently - always handle errors gracefully
- Custom exceptions make debugging way easier than generic error messages
- Logging to files means you can track issues even after deployment
- `try/except` blocks separate normal flow from error handling

---

### Day 7: File Handling & JSON Persistence

**What I Built:** Added the ability to save and load account data using JSON files

Now the banking system can remember everything even after you close it! Implemented save/load functionality so accounts and transactions persist between program runs. Had to learn how to convert Python objects to JSON and back - turns out datetime objects need special handling.

```python
# Serialization - Converting Python objects to JSON
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
            json.dump(data_to_save, f, indent=4)
        logging.info("All accounts saved successfully.")
    except Exception as e:
        logging.error(f"Error saving accounts: {str(e)}")

# Deserialization - Converting JSON back to Python objects
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
        logging.warning(f"{filename} not found. Starting fresh.")
    return accounts
```

```bash
python day07/persistent_bank.py
# Close the program, run again - data is still there!
```

**What I Learned:**

_Serialization:_ Converting your Python objects (like classes and datetime) into a format that can be saved to a file. Think of it like packing your stuff into boxes before moving - you're converting it into a storable format.

_Deserialization:_ The opposite - reading the saved file and recreating your Python objects from it. Like unpacking boxes and putting everything back where it belongs.

_Context Managers (`with` statement):_ Automatically closes files even if errors occur. Like a door that locks itself when you leave - you don't have to remember to close it manually.

**Key Takeaways:**

- JSON is perfect for saving simple data structures between program runs
- Always handle `FileNotFoundError` - the file might not exist on first run
- Context managers (`with open()`) automatically clean up resources
- Datetime objects need to be converted to strings for JSON compatibility

---

## Project Structure

```
backend-journey/
├── day01/          # Environment setup
├── day02/          # Calculator with modules
├── day03/          # Basic bank account
├── day04/          # Banking with inheritance
├── day05/          # Dataclasses & type hints
├── day06/          # Exception handling & logging
├── day07/          # JSON persistence
└── requirements.txt
```

## What's Next

**Week 2** - Starting Monday with a CLI task manager project

The long-term roadmap: REST APIs, SQL/NoSQL databases, authentication, Docker, and eventually deploying production applications.

---
