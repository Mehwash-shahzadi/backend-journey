# 90-Day Backend Engineering Journey

## Why This Challenge?

I've been dabbling with Python for a while, but never had the structure to become job-ready. So I'm committing to 90 days - 2 hours daily, building real projects instead of following tutorials.

**Goal:** Go from writing scripts to building production-grade backend applications. By day 90, I want to confidently apply for backend developer roles.

This repo is my public accountability. Week 2 complete. Now diving into FastAPI and REST APIs (Week 3). Let's see where this goes.

## Quick Start

```bash
git clone https://github.com/Mehwash-Shahzadi/backend-journey.git
cd backend-journey
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Try the Task Manager:**

```bash
cd day12-14/task_manager_final
python main.py add "Your first task" --priority HIGH --tags work,urgent
python main.py list
python main.py stats
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

#### Day 2: Modules & Packages

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

#### Day 3: OOP Basics

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

#### Day 4: Inheritance & Composition

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

#### Day 5: Dataclasses & Type Hints

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

#### Day 6: Exception Handling & Logging

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

#### Day 7: File Handling & JSON Persistence

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

## Week 2: Building Real Applications

### Day 8-9: CLI Task Manager Project

**What I Built:** A complete command-line task manager with CRUD operations

This was the big one - combined everything from Week 1 into a real application. Built a full task manager that you can use from the terminal. It has add, list, complete, and delete commands. All data persists to JSON, and you can filter by status or sort by date.

**Why CLI Tools Matter in Backend:**

CLI (Command Line Interface) tools are everywhere in backend development. Think of them as text-based apps that run in the terminal instead of having buttons and windows. Here's why they're important:

- **DevOps & Automation:** Backend engineers use CLI tools daily - deploying apps (`git push`), managing databases (`psql`), running migrations, checking logs
- **Server Management:** Most servers don't have a visual interface. Everything happens through terminal commands
- **Scripts & Automation:** CLI tools can be called from scripts, scheduled tasks (cron jobs), or CI/CD pipelines
- **How They Work:** User types a command → CLI parses it → Your code executes → Results display in terminal

Real examples: `docker run`, `npm install`, `pytest`, `aws s3 sync`. All CLI tools. Building one teaches you how to structure commands, handle user input, and create reusable tools - essential backend skills.

**Project Structure:**

```
day08-09/task_manager/
├── models.py        # Task dataclass
├── manager.py       # TaskManager with CRUD logic
├── storage.py       # JSON persistence
├── cli.py           # Click-based CLI interface
├── main.py          # Entry point
└── tasks.json       # Auto-generated data file
```

**Key Code Snippets:**

_Task Model (models.py):_

```python
@dataclass
class Task:
    id: int
    title: str
    status: str = "pending"
    created_at: datetime = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
```

_CLI Interface (cli.py):_

```python
@click.group()
def cli():
    """Simple CLI Task Manager"""
    pass

@cli.command()
@click.argument("title")
def add(title):
    """Add a new task"""
    task = manager.add(title)
    save_to_file(TASKS_FILE, manager)
    click.echo(f"Task added: {task.title} (id={task.id})")

@cli.command(name="list")
@click.option("--status", type=click.Choice(["pending", "completed"]))
@click.option("--sort", type=click.Choice(["asc", "desc"]), default="asc")
def list_tasks(status, sort):
    """List tasks with filtering and sorting"""
    tasks = manager.list()
    if status:
        tasks = [t for t in tasks if t.status == status]
    tasks.sort(key=lambda t: t.created_at, reverse=(sort == "desc"))
    for task in tasks:
        click.echo(f"[{task.id}] {task.title} - {task.status}")
```

**Usage Examples:**

```bash
# Add tasks
python main.py add "Buy groceries"
python main.py add "Finish Day 9 exercises"

# List all tasks
python main.py list

# List only pending tasks, sorted newest first
python main.py list --status pending --sort desc

# Complete a task
python main.py complete 1

# Delete a task
python main.py delete 2
```

**What I Learned:**

_CLI Arguments:_ Click library makes it easy to build professional command-line tools. Arguments are required values, options are optional flags.

_CRUD Operations:_ Create, Read, Update, Delete - the fundamental operations for managing data. Every backend system needs these.

_Project Organization:_ Splitting code into separate files (models, manager, storage, cli) makes it maintainable. Each file has one clear responsibility.

**Key Takeaways:**

- Click is way better than raw `argparse` for building CLIs
- Separating concerns (models/manager/storage/cli) makes debugging easier
- Options with `click.Choice()` prevent invalid user input
- This project is basically a mini backend - just without HTTP/database

---

### Day 10-11: Magic Methods & Design Patterns

**What I Built:** Made the task manager smarter with Python's special methods and flexible sorting

Learned about "magic methods" (those functions with double underscores like `__str__`) and the Strategy pattern. Now tasks can be compared, sorted, and printed naturally. Plus, I can switch between different sorting methods without rewriting code.

**What Are Magic Methods?**

Magic methods are special functions in Python that start and end with `__` (double underscores). They let you teach Python how to work with your custom classes.

Think of it like this: When you do `len([1, 2, 3])`, Python calls the list's `__len__` method behind the scenes. Now your own classes can do the same!

**Magic Methods I Added:**

```python
@dataclass
class Task:
    id: int
    title: str
    priority: int = 1
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self):
        """What you see when you print(task)"""
        return f"{self.id}. {self.title} ({self.status}, priority={self.priority})"

    def __repr__(self):
        """What you see in the debugger - shows all details"""
        return f"Task(id={self.id}, title='{self.title}', priority={self.priority})"

    def __eq__(self, other):
        """How Python checks if two tasks are equal: task1 == task2"""
        return self.id == other.id

    def __lt__(self, other):
        """How Python compares tasks for sorting: task1 < task2"""
        return self.created_at < other.created_at
```

**Making TaskManager Iterable:**

```python
class TaskManager:
    def __len__(self):
        """Now you can use: len(manager)"""
        return len(self.tasks)

    def __getitem__(self, index):
        """Now you can use: manager[0] or loop with 'for task in manager'"""
        return self.tasks[index]
```

**Usage:**

```python
manager = TaskManager()
manager.add("Buy groceries", priority=2)
manager.add("Walk dog", priority=1)

# Magic methods in action!
print(len(manager))           # Works because of __len__
for task in manager:          # Works because of __getitem__
    print(task)               # Works because of __str__

# Comparing tasks
if manager[0] == manager[1]:  # Works because of __eq__
    print("Same task!")
```

**What Is the Strategy Pattern?**

The Strategy pattern is a way to make your code flexible. Instead of hardcoding one way to do something (like sorting), you create different "strategies" that can be swapped in and out.

**Simple analogy:** Your phone has different modes - Silent, Vibrate, Ring. Same phone, different behaviors. That's Strategy pattern!

**How I Implemented It:**

```python
# Different sorting strategies
class SortByDate:
    """Sort tasks by when they were created"""
    def sort(self, tasks):
        return sorted(tasks, key=lambda t: t.created_at)

class SortByPriority:
    """Sort tasks by priority (higher numbers first)"""
    def sort(self, tasks):
        return sorted(tasks, key=lambda t: t.priority, reverse=True)

# TaskManager accepts any sorting strategy
class TaskManager:
    def __init__(self, sorter=None):
        self.tasks = []
        self.sorter = sorter  # Can be SortByDate or SortByPriority

    def list(self):
        """Returns tasks using whatever sorting strategy was chosen"""
        if self.sorter:
            return self.sorter.sort(self.tasks)
        return self.tasks
```

**Usage:**

```python
# Create two managers with different sorting
manager1 = TaskManager(sorter=SortByDate())
manager2 = TaskManager(sorter=SortByPriority())

# Same tasks, different order!
manager1.list()  # Sorted by date
manager2.list()  # Sorted by priority
```

**Why This Matters:**

_Magic Methods:_ Make your classes feel natural to use. Instead of `task.get_length()`, you just use `len(task)`. Makes code cleaner and more "Pythonic."

_Strategy Pattern:_ Keeps code flexible. Want to add "SortByStatus" later? Just create a new class. No need to touch existing code. This is called "Open/Closed Principle" - open for extension, closed for modification.

**Key Takeaways:**

- `__str__` = what users see, `__repr__` = what developers see while debugging
- `__eq__` and `__lt__` let Python know how to compare your objects
- `__len__` and `__getitem__` make your class work like a list
- Strategy pattern = swappable behaviors without changing main code
- Real-world use: FastAPI uses this pattern for dependency injection

---

### Day 12-14: Final Polish & Production Ready

**What I Built:** Completed the task manager with professional features and beautiful UI

Added all the finishing touches that make this portfolio-ready. Now it has priority levels using Enums, tag filtering, CSV export for data portability, statistics dashboard, and gorgeous terminal output with Rich library. Every function has documentation. This is now a production-quality project.

**What Are Enums?**

Enums (Enumerations) are a way to define a set of named constants. Instead of using strings like "HIGH", "MEDIUM", "LOW" everywhere (which can have typos), you create an Enum that limits the choices.

**Think of it like:** A dropdown menu. You can only select from the options given - no typos, no invalid values.

**Priority System with Enums:**

```python
from enum import Enum

class Priority(Enum):
    """Only these three values are allowed"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass
class Task:
    id: int
    title: str
    priority: Priority = Priority.MEDIUM  # Must be one of the Enum values
    tags: List[str] = field(default_factory=list)  # Can add multiple tags
```

**Why Enums are Better:**

```python
#  Without Enum - Typos can happen
task.priority = "HIHG"  # Typo! Will cause bugs later

#  With Enum - IDE catches mistakes
task.priority = Priority.HIGH  # Autocomplete helps, typos impossible
```

**CSV Export - Taking Your Data Elsewhere:**

```python
def export_to_csv(self, filename: str = "tasks_export.csv") -> None:
    """Export all tasks to a CSV file that Excel/Google Sheets can open"""
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Header row
        writer.writerow(["id", "title", "status", "created_at", "priority", "tags"])
        # Data rows
        for t in self.tasks:
            writer.writerow([
                t.id,
                t.title,
                t.status,
                t.created_at.isoformat(),
                t.priority.value,  # Get the string value from Enum
                ";".join(t.tags)   # Combine tags into one cell
            ])
```

**Statistics Dashboard:**

```python
def statistics(self, overdue_days: int = 7) -> dict:
    """Calculate task stats - total, completed, overdue"""
    total = len(self.tasks)
    completed = sum(1 for t in self.tasks if t.status == "completed")
    completed_pct = (completed / total * 100) if total else 0.0

    # Find overdue tasks (pending for more than X days)
    cutoff = datetime.now() - timedelta(days=overdue_days)
    overdue = sum(1 for t in self.tasks
                  if t.status == "pending" and t.created_at < cutoff)

    return {
        "total": total,
        "completed": completed,
        "completed_pct": round(completed_pct, 2),
        "overdue": overdue
    }
```

**Rich Library - Beautiful Terminal Output:**

```python
from rich.console import Console
from rich.table import Table

console = Console()

def display_tasks(tasks):
    """Show tasks in a pretty table with colors"""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Title")
    table.add_column("Priority")
    table.add_column("Status")
    table.add_column("Tags")

    for t in tasks:
        # Color code priorities: HIGH=red, MEDIUM=yellow, LOW=green
        pri_color = "red" if t.priority == Priority.HIGH else \
                    ("yellow" if t.priority == Priority.MEDIUM else "green")

        table.add_row(
            str(t.id),
            t.title,
            f"[{pri_color}]{t.priority.value}[/{pri_color}]",
            t.status,
            ", ".join(t.tags)
        )

    console.print(table)
```

**Advanced Filtering in CLI:**

```bash
# Filter by multiple criteria
python main.py list --status pending --priority HIGH --tag urgent

# Sort by priority instead of date
python main.py list --sort priority --desc

# Export everything to CSV
python main.py export tasks_export.csv

# See statistics
python main.py stats --overdue-days 3
```

**Demo:**

![Task Manager Demo](day12-14/demo.gif)

**What I Learned:**

_Enums:_ They're like safety rails. Once you define the valid options, Python won't let you use anything else. Prevents bugs from typos and invalid values.

_CSV Export:_ Universal format - works with Excel, Google Sheets, pandas, any data tool. Good for sharing data or importing into other systems.

_Rich Library:_ Transforms boring terminal output into beautiful tables with colors. Makes CLI apps feel professional and easier to read.

_Statistics:_ Real apps need metrics. Users want to know: How many tasks? Completion rate? What's overdue? Simple math, big impact.

**Project Structure:**

```
day12-14/task_manager_final/
├── models.py           # Task class with Enums and magic methods
├── manager.py          # TaskManager with filtering, stats, CSV export
├── strategies.py       # SortByDate and SortByPriority
├── storage.py          # JSON save/load
├── cli.py              # Rich-powered CLI with Click
├── main.py             # Entry point
├── tasks.json          # Auto-generated data file
├── tasks_export.csv    # Example CSV export
└── demo.gif            # Demo showing the app in action
```

**Key Takeaways:**

- Enums prevent invalid values and make code self-documenting
- CSV export makes your data portable to other tools
- Rich library turns terminal apps from ugly to beautiful
- Statistics give users insight into their data
- Good documentation and demos make projects portfolio-ready

---

## Week 2 Wrap-Up

**What I Built This Week:**

- Full-featured CLI task manager with CRUD operations
- Magic methods making classes feel Pythonic
- Strategy pattern for flexible sorting
- Enums for type safety
- CSV export and statistics
- Beautiful Rich terminal UI
- Complete documentation

**Skills Gained:**

- Advanced OOP (magic methods, design patterns)
- CLI development with Click
- Data export and statistics
- Terminal UI design with Rich
- Clean code principles
- Professional documentation

This project is now portfolio-ready and demonstrates real backend engineering skills.

---

## Week 3: FastAPI Fundamentals

### Day 15: HTTP Basics & FastAPI Setup

**What I Built:** My first REST API with FastAPI

Started learning web APIs today. FastAPI makes it surprisingly easy to create endpoints that respond to HTTP requests. Set up a basic API server with three different routes - one simple hello world, one with path parameters, and one with query parameters.

**What is HTTP and REST API?**

HTTP (HyperText Transfer Protocol) is how browsers and apps talk to servers. When you visit a website, your browser sends an HTTP request, the server processes it, and sends back a response.

REST API is a way to structure these conversations. Think of it like a restaurant menu - each endpoint is a dish you can order, and HTTP methods (GET, POST, PUT, DELETE) are how you place your order.

**HTTP Methods I Learned:**

- GET: Retrieve data (like reading a menu)
- POST: Create new data (like placing an order)
- PUT: Update existing data (like changing your order)
- DELETE: Remove data (like canceling an order)

**My First FastAPI App:**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    """Simple Hello World endpoint"""
    return {"Hello": "World"}

# Path parameter - part of the URL
@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Get item by ID"""
    return {"item_id": item_id}

# Query parameter - like filtering options
@app.get("/search")
def search_items(query: str = None, limit: int = 10):
    """Search items with optional query and limit"""
    return {"query": query, "limit": limit}
```

**Running the API:**

```bash
cd day15/first_api
uvicorn main:app --reload
```

Then visit:

- `http://localhost:8000/` - See hello world
- `http://localhost:8000/items/42` - Path parameter example
- `http://localhost:8000/search?query=phone&limit=5` - Query parameters
- `http://localhost:8000/docs` - Auto-generated documentation

**What I Learned:**

_Path Parameters:_ Part of the URL itself. Like `/users/123` where 123 is the user ID. Used for identifying specific resources.

_Query Parameters:_ Come after `?` in the URL. Like `/search?query=hello&limit=10`. Used for filtering or options.

_Auto-Generated Docs:_ FastAPI automatically creates interactive documentation at `/docs`. You can test your API right in the browser without Postman.

**Screenshots:**

**Hello World Endpoint:**

![Hello World Response](day15/screenshots/hello_world.png)

**Path Parameter Example (`/items/{item_id}`):**

![Path Parameter](day15/screenshots/item_id.png)

**Query Parameters Example (`/search?query=phone&limit=5`):**

![Query Parameters](day15/screenshots/search.png)

**Auto-Generated API Documentation (`/docs`):**

![Auto Docs](day15/screenshots/docs.png)

**Key Takeaways:**

- FastAPI uses Python type hints to validate data automatically
- Path parameters are for identifying resources, query parameters are for filtering
- The `/docs` endpoint gives you free interactive API documentation
- `uvicorn --reload` automatically restarts the server when you change code

---

### Day 16: Pydantic Models & Validation

**What I Built:** Added data validation with Pydantic models

Today was about making the API smarter. Instead of accepting any random data, I used Pydantic models to define exactly what structure the data should have. Now the API automatically validates emails, checks password length, and rejects bad data before it even reaches my code.

**What is Pydantic?**

Pydantic is a data validation library. You define what your data should look like using Python classes, and Pydantic makes sure incoming data matches that structure.

Think of it like a bouncer at a club checking IDs. If the data doesn't match the rules, it doesn't get in.

**Why Separate Request and Response Models?**

Request model: What the client sends (includes password)
Response model: What we send back (excludes sensitive data like passwords)

This keeps passwords and sensitive info from accidentally being sent back to users.

**User Models with Validation:**

```python
from pydantic import BaseModel, EmailStr, Field

# What we accept when creating a user
class UserCreate(BaseModel):
    email: EmailStr                    # Must be valid email format
    password: str = Field(min_length=8)  # At least 8 characters
    age: int = Field(gt=0)              # Must be greater than 0

# What we send back (no password!)
class UserResponse(BaseModel):
    email: EmailStr
    age: int
```

**API Endpoint Using Models:**

```python
from fastapi import FastAPI
from models import UserCreate, UserResponse

app = FastAPI()

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    """Create a new user"""
    # Pydantic already validated the data
    # We return only safe fields
    return UserResponse(
        email=user.email,
        age=user.age
    )
```

**Testing Validation:**

Valid request:

```json
{
  "email": "user@example.com",
  "password": "secure123",
  "age": 25
}
```

Response: Success!

Invalid request:

```json
{
  "email": "not-an-email",
  "password": "short",
  "age": -5
}
```

Response: Validation error with details about what's wrong

**What I Learned:**

_EmailStr:_ Pydantic's special type that validates email format automatically. Rejects "notanemail" but accepts "user@example.com".

_Field Validators:_ `min_length=8` means password must be at least 8 characters. `gt=0` means age must be greater than zero.

_Automatic Validation:_ If data is invalid, FastAPI returns a 422 error with details before your function even runs. You don't have to write validation code.

_Security:_ Using separate response models prevents accidentally leaking passwords or other sensitive data.

**Key Takeaways:**

- Pydantic models define the shape of your data
- Validation happens automatically - no manual checks needed
- Always use separate request/response models for security
- Field validators make rules explicit and self-documenting
- Invalid data gets rejected with helpful error messages

---

## Project Structure

```
backend-journey/
├── day01/              # Environment setup
├── day02/              # Calculator with modules
├── day03/              # Basic bank account
├── day04/              # Banking with inheritance
├── day05/              # Dataclasses & type hints
├── day06/              # Exception handling & logging
├── day07/              # JSON persistence
├── day08-09/           # CLI Task Manager
│   └── task_manager/
├── day10-11/           # Magic Methods & Strategy Pattern
│   └── task_manager_v2/
├── day12-14/           # Production-Ready Task Manager
│   └── task_manager_final/
├── day15/              # First FastAPI App
│   ├── first_api/
│   │   └── main.py
│   └── screenshots/
│       ├── docs.png
│       ├── hello_world.png
│       ├── item_id.png
│       └── search.png
├── day16/              # Pydantic Models & Validation
│   └── user_api/
│       ├── main.py
│       └── models.py
└── requirements.txt
```

## What's Next

**Day 17-18** - Async programming, database setup with PostgreSQL, SQLAlchemy basics

**Week 4** - Building a complete CRUD API with database integration, relationships, and migrations

The roadmap ahead: Authentication & JWT tokens, Docker containers, pytest for testing, CI/CD pipelines, and cloud deployment.

---
