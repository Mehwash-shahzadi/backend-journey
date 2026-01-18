# 90-Day Backend Engineering Journey

## Why This Challenge?

I've been dabbling with Python for a while, but never had the structure to become job-ready. So I'm committing to 90 days - 2 hours daily, building real projects instead of following tutorials.

**Goal:** Go from writing scripts to building production-grade backend applications. By day 90, I want to confidently apply for backend developer roles.

This repo is my public accountability. Week 10-11 complete. Moving forward!

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
# Without Enum - Typos can happen
task.priority = "HIHG"  # Typo! Will cause bugs later

# With Enum - IDE catches mistakes
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

### Day 17: CRUD Operations

**What I Built:** Full REST API with Create, Read, Update, Delete operations

Built a complete CRUD API using in-memory storage (Python list). This helped me focus on REST conventions and HTTP status codes without database complexity yet.

```python
@app.post("/users", status_code=201)
async def create_user(user: UserCreate):
    user_id = len(users) + 1
    new_user = UserResponse(id=user_id, name=user.name, email=user.email, age=user.age)
    users.append(new_user)
    return new_user

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")
```

**What I Learned:**

_CRUD:_ Create (POST), Read (GET), Update (PUT), Delete (DELETE) - the four basic operations for any data-driven app.

_REST Conventions:_ URLs are resources (nouns like `/users`), HTTP methods are actions (verbs like GET, POST).

_Status Codes:_ 200 (success), 201 (created), 404 (not found), 422 (validation error).

**Key Takeaways:**

- CRUD is 80% of backend work
- Use proper status codes - 201 for creation, 404 for not found
- HTTPException returns formatted error responses

---

### Day 18: Async Programming

**What I Built:** Converted API to async and added concurrent request handling

Learned async/await - a way to handle multiple requests simultaneously without blocking.

```python
@app.get("/slow")
async def slow_endpoint():
    await asyncio.sleep(2)  # Simulate database wait
    return {"message": "Done"}

@app.get("/external")
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/users")
    return response.json()
```

**What I Learned:**

_Async/Await:_ Lets server handle other requests while waiting for I/O (database, API calls). Like chopping vegetables while water boils instead of just watching it.

_When to Use:_ Database queries, external API calls, file operations. Not for CPU-heavy calculations.

**Key Takeaways:**

- Async handles more concurrent users, not faster single requests
- Use `async def` for routes, `await` for I/O operations
- FastAPI handles async automatically

---

### Day 19: Dependency Injection

**What I Built:** Reusable dependencies for pagination and validation

Dependency Injection = write validation/logic once, reuse everywhere.

```python
def get_pagination(skip: int = 0, limit: int = 10):
    if skip < 0 or limit <= 0:
        raise HTTPException(status_code=400, detail="Invalid params")
    return {"skip": skip, "limit": limit}

@app.get("/users")
async def get_users(pagination: dict = Depends(get_pagination)):
    skip = pagination["skip"]
    limit = pagination["limit"]
    return users[skip:skip + limit]
```

**What I Learned:**

_Depends():_ FastAPI calls the dependency function automatically. No need to manually call it.

_Common Uses:_ Pagination, authentication, database connections, user validation.

**Key Takeaways:**

- Dependencies keep code DRY (Don't Repeat Yourself)
- Cleaner routes - focus on business logic, not validation
- Essential for larger APIs

---

### Day 20: Background Tasks & Middleware

**What I Built:** Background tasks for emails, middleware for logging

Background tasks run after the response. Middleware runs on every request.

```python
async def send_email(email: str):
    await asyncio.sleep(2)
    logging.info(f"Email sent to {email}")

@app.post("/users")
async def create_user(user: UserCreate, background_tasks: BackgroundTasks):
    user_data = save_user(user)
    background_tasks.add_task(send_email, user.email)
    return user_data  # Immediate response, email sends later

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logging.info(f"{request.method} {request.url.path} - {duration:.2f}s")
    return response
```

**What I Learned:**

_Background Tasks:_ User gets fast response, slow work (emails, cleanup) happens after.

_Middleware:_ Runs automatically on every request. Good for logging, authentication, timing.

**Key Takeaways:**

- Background tasks keep responses fast
- Middleware adds functionality to all routes at once
- Production pattern for non-critical operations

---

### Day 21: PostgreSQL Setup

**What I Built:** Installed PostgreSQL and practiced SQL

Set up PostgreSQL locally and learned basic SQL commands.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO users (email, name) VALUES ('user@example.com', 'John');
SELECT * FROM users;
UPDATE users SET name = 'Jane' WHERE id = 1;
DELETE FROM users WHERE id = 1;
```

**What I Learned:**

_SQL Basics:_ SELECT (read), INSERT (create), UPDATE (modify), DELETE (remove).

_SERIAL:_ Auto-incrementing ID. Database assigns 1, 2, 3 automatically.

_Constraints:_ UNIQUE prevents duplicates, NOT NULL requires a value.

**Key Takeaways:**

- SQL is the language for databases
- Learn SQL before ORMs - helps with debugging
- PostgreSQL is industry standard, free and powerful

---

---

### Day 22: SQLAlchemy ORM Basics

**What I Built:** Replaced raw SQL with SQLAlchemy ORM

Instead of writing SQL queries manually, I learned to use SQLAlchemy - a tool that lets you work with databases using Python classes. Way cleaner than string concatenation.

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("postgresql://user:pass@localhost/fastapi_db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**What I Learned:**

_ORM:_ Object-Relational Mapping. Instead of `SELECT * FROM users`, you write `session.query(User).all()`. Database tables become Python classes.

_Session:_ Like a workspace for database operations. Open it, do your work, commit changes, close it.

**Key Takeaways:**

- ORMs make database code more readable and maintainable
- SQLAlchemy is Python's standard ORM - used everywhere
- Type safety - IDE can autocomplete database fields

---

### Day 23: FastAPI + SQLAlchemy Integration

**What I Built:** Connected FastAPI routes to real PostgreSQL database

Integrated yesterday's SQLAlchemy code with FastAPI. Now the API actually saves data to PostgreSQL instead of a Python list that disappears when the server restarts.

```python
# dependencies.py
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# main.py
@app.post("/users")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

**What I Learned:**

_get_db() Dependency:_ Creates a database session for each request, automatically closes it after. Prevents connection leaks.

_Session Management:_ Add (stage), commit (save), refresh (get updated data from DB).

**Key Takeaways:**

- Every route gets its own database session via dependency injection
- Always close sessions to avoid connection leaks
- This pattern is used in every production FastAPI app

---

### Day 24: Database Relationships

**What I Built:** Added Posts table with relationships to Users

Real apps have related data - users have posts, posts have comments. Learned how to model these relationships in SQLAlchemy.

```python
# models.py
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    posts = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="posts")

# Get user with all their posts
@app.get("/users/{user_id}/posts")
async def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user.posts
```

**What I Learned:**

_Foreign Key:_ Links tables together. `user_id` in posts table references `id` in users table.

_relationship():_ SQLAlchemy magic that lets you access related data easily. `user.posts` automatically fetches all posts by that user.

**Key Takeaways:**

- Relationships represent real-world connections between data
- Foreign keys maintain data integrity at database level
- ORM relationships prevent manual join queries

---

### Day 25-26: Complete Blog API Project

**What I Built:**  
Production-quality API with users, posts, and comments. Organized code with separate folders for models, routes, and CRUD logic.

**See full documentation and project details here:**  
[blog_api README](day25-26/blog_api/README.md)

---

### Day 27-28: Blog API – Final Polish & Documentation

**What I Built:**  
Polished version of the Blog API from Day 25–26 with docstrings, OpenAPI docs, seed data, and environment setup.

Spent two days making the blog API production-ready. Added comprehensive documentation, environment variable setup, and a seeding script to quickly populate test data.

**Key Improvements:**

- Detailed docstrings for every function
- Enhanced OpenAPI docs with examples
- Environment variable configuration (.env file)
- Database seeding script for testing
- Professional README with full API documentation
  **What I Learned:**

_Good Documentation:_ Makes your code usable by others (and your future self). Includes setup instructions, API examples, and error handling.

_Environment Variables:_ Never hardcode passwords or API keys. Use `.env` files for configuration.

_Seeding Scripts:_ Populate database with test data for development and demos.

**Key Takeaways:**

- Documentation quality separates junior from mid-level developers
- FastAPI's auto-generated docs get better with proper descriptions
- Environment configuration makes deployment easier

**See full documentation and project details here:**  
[blog_api_final README](day27-28/blog_api_final/README.md)

## Week 3-4 Complete

**What I Built These Two Weeks:**

- REST APIs with FastAPI (20+ endpoints)
- PostgreSQL database with relationships
- Complete blog API (users, posts, comments)
- Async operations and background tasks
- Production-ready project structure
- Comprehensive documentation

**Skills Mastered:**

- FastAPI framework
- SQLAlchemy ORM
- Database design and relationships
- API architecture
- Professional documentation
- Environment configuration

This blog API is now portfolio-ready and demonstrates real-world backend engineering skills.

---

---

### WEEK 5-6: Database Layer & ORM Mastery

### Day 29: Database Migrations with Alembic

**What I Built:** Learned to manage database schema changes with Alembic

Today was about version control for databases. Alembic tracks changes to your database schema - when you add columns, create tables, or modify structures. It creates migration files that can be applied to any database, keeping everyone in sync.

**Why Migrations Matter:**

Without migrations, you'd manually run SQL commands on every database (development, staging, production). Miss one and things break. With migrations, changes are tracked in code and applied consistently everywhere.

**Basic Workflow:**

```bash
# 1. Change your SQLAlchemy model (add a field)
# 2. Generate migration file
alembic revision --autogenerate -m "Add bio to users"

# 3. Apply to database
alembic upgrade head

# 4. Rollback if needed
alembic downgrade -1
```

**What I Learned:**

_Migrations:_ Like Git commits for your database. Each migration file describes what changed.

_Autogenerate:_ Alembic compares your models to the current database and creates migration code automatically.

_Upgrade/Downgrade:_ Apply changes forward or roll them back. Critical for fixing mistakes in production.

**Key Takeaways:**

- Never modify production databases manually
- Migrations keep teams synchronized on schema changes
- Always test migrations on development databases first
- Version control migration files with Git

**Detailed Migration Guide:**
View [Complete Alembic Tutorial](day29/migrations_practice/README.md) for step-by-step commands and troubleshooting.

---

### Day 30: Advanced Queries and Filtering

**What I Built:** Search and filtering system for blog posts

Added advanced querying - search by text, filter by author/date/tags, and sort results. Implemented database indexes for fast queries.

```bash
# Example queries
GET /posts/?search=python
GET /posts/?author=mehwash&sort=created_at&order=desc
GET /posts/?from_date=2025-01-01&to_date=2025-12-31
GET /posts/?tags=python,fastapi
```

**What I Learned:**

_Dynamic Filtering:_ Build queries based on provided parameters using SQLAlchemy's filter chaining.

_Database Indexes:_ Speed up queries significantly on frequently searched columns.

**Key Takeaways:**

- SQLAlchemy allows dynamic query building
- Indexes are critical for production performance
- Support multiple optional filters for better UX

**Complete Guide:**
[View Advanced Filtering Tutorial](day30/advanced_queries/README.md)

---

### Day 31: Database Transactions

**What I Built:** Money transfer system demonstrating atomic operations

Built a transfer system to learn transactions - operations that must complete fully or not at all. If transferring money between users fails at any step, everything rolls back automatically.

**Key Concepts:**

```python
# Transaction example
try:
    sender.balance -= amount
    receiver.balance += amount
    db.commit()  # Save both changes
except Exception:
    db.rollback()  # Undo everything if anything fails
```

**What I Learned:**

_Atomicity:_ All-or-nothing operations. Either both balances update or neither does. Prevents partial updates that corrupt data.

_Commit/Rollback:_ `commit()` saves changes, `rollback()` undoes them. Critical for maintaining data consistency.

_Unique Constraints:_ Database-level enforcement prevents duplicate emails or IDs automatically.

**Test Scenarios:**

- Successful transfer - both balances update
- Insufficient funds - rollback, no changes
- User not found - rollback, no changes
- Duplicate email - database prevents insertion

**Key Takeaways:**

- Transactions prevent data corruption in multi-step operations
- Always wrap related database operations in transactions
- Let database rollback on errors automatically
- Critical for banking, e-commerce, inventory systems

---

### Day 34: Async SQLAlchemy

**What I Built:** Converted entire database layer from synchronous to asynchronous operations

Transformed the application to handle database operations asynchronously. Instead of blocking while waiting for database responses, the server can now handle thousands of concurrent requests efficiently.

**Key Concepts:**

```python
# Sync (blocks server)
def get_users(db: Session):
    return db.query(User).all()  # Server waits here

# Async (non-blocking)
async def get_users(db: AsyncSession):
    result = await db.execute(select(User))  # Server handles other requests
    return result.scalars().all()
```

**What I Learned:**

_async/await:_ `async def` marks functions as pausable. `await` tells Python "pause here, handle other requests, come back when ready."

_AsyncSession:_ Replaces regular Session for non-blocking database operations. Uses `asyncpg` driver instead of `psycopg2`.

_Contagious Pattern:_ If repository is async → service must be async → router must be async. The entire chain must support async.

_Performance Gain:_ One server can handle 100 concurrent requests in 2-3 seconds vs 200 seconds with sync code.

**Key Changes:**

```python
# Database setup
create_async_engine()           # Instead of create_engine()
AsyncSession                    # Instead of Session
postgresql+asyncpg://           # Instead of postgresql://

# Query execution
await db.execute(select(User))  # Instead of db.query(User)
await db.commit()               # Instead of db.commit()
await db.refresh(user)          # Instead of db.refresh(user)
```

**Key Takeaways:**

- Async dramatically improves performance for I/O-bound operations (database, APIs, files)
- Use `await` before any operation that talks to database or external services
- Every function in the call chain must be async (router → service → repository)
- Essential for high-traffic applications with hundreds of concurrent users

---

### Day 35: Many-to-Many Relationships

**What I Built:** Posts and Tags system with many-to-many relationship

Implemented a blog-style system where posts can have multiple tags and tags can belong to multiple posts. This required an association table to manage the relationship.

**Key Concepts:**

```python
# Association table
post_tags = Table(
    'post_tags',
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

# Models with relationship
class Post(Base):
    tags = relationship("Tag", secondary=post_tags, back_populates="posts", lazy="selectin")

class Tag(Base):
    posts = relationship("Post", secondary=post_tags, back_populates="tags", lazy="selectin")
```

**What I Learned:**

_Association Table:_ Junction table that connects two tables in many-to-many relationships. Contains only foreign keys, no primary key of its own.

_secondary Parameter:_ Tells SQLAlchemy which table manages the relationship. Allows accessing `post.tags` and `tag.posts` directly.

_back_populates:_ Creates bidirectional relationship. Can navigate from Post to Tags and Tags to Posts.

_lazy="selectin":_ Critical for async! Eagerly loads relationships automatically, preventing "MissingGreenlet" errors in async code.

**Async-Specific Challenge:**

```python
# Problem: Lazy loading doesn't work in async
result = await db.execute(select(Post))
posts = result.scalars().all()
# posts.tags causes error - relationship not loaded!

# Solution: Use lazy="selectin" in model
lazy="selectin"  # Auto-loads relationships in async
```

**API Endpoints Built:**

- `POST /tags` - Create new tag
- `POST /posts/{id}/tags` - Add existing tag to post
- `GET /tags/{id}/posts` - Get all posts with specific tag
- `GET /posts` - List posts with their tags
- `POST /posts` - Create new post

**Key Takeaways:**

- Many-to-many requires three tables: two entity tables + one association table
- Always use `lazy="selectin"` for relationships in async SQLAlchemy
- Association tables make complex relationships simple to query
- Essential pattern for: products↔categories, users↔groups, students↔courses

---

### Day 36-38: E-Commerce API

**What I Built:** Complete e-commerce backend with production patterns

Built a full online store backend demonstrating complex relationships and business logic.

**Core Features:**

- Product catalog with categories (many-to-many)
- Order system with stock validation
- Atomic transactions (all-or-nothing)
- Price snapshots for order history
- Admin/customer roles

**Order Flow:**

```
Validate → Check Stock → Calculate → Reduce Stock →
Create Order → Rollback if Fails
```

**Architecture:**

- Repository pattern (data access)
- Service layer (business logic)
- Async SQLAlchemy
- Alembic migrations

**What I Learned:**

_Repository Pattern:_ Separates database code from business logic. Makes testing easier.

_Service Layer:_ All business rules in one place. Handles validation and transactions.

_Atomic Transactions:_ Multiple operations succeed together or fail together. Critical for orders.

**Key Takeaways:**

- Large projects need clear architecture
- Transactions prevent data corruption
- Many-to-many needs association tables
- Real apps need careful validation

[View Complete Documentation](day36-38/ecommerce_api/README.md)

---

## Week 7-8: Modular Architecture & Authentication

### Day 43: Modular Architecture

**What I Built:** Refactored the e-commerce API into a clean modular structure

Reorganized the entire project from a messy folder structure into professional modules. Each feature (users, products, orders) now lives in its own self-contained module.

**New Structure:**

```
app/
├── modules/
│   ├── users/              # User module
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   └── router.py
│   ├── products/           # Product module
│   └── orders/             # Order module
├── shared/                 # Shared utilities
│   ├── exceptions.py
│   ├── utils.py
│   └── middleware.py
└── main.py                 # App factory
```

**What I Learned:**

_Modular Monolith:_ One application but organized into independent modules. Easier than microservices but cleaner than a single file.

_Separation of Concerns:_ Each module has its own models, routes, and logic. Changes to users don't affect products.

_App Factory Pattern:_ `main.py` registers all module routers. Adding new features means creating a new module folder.

**Key Takeaways:**

- Each module is self-contained and independent
- Shared code goes in `shared/` folder
- Easy to work on teams - assign one module per person
- Scales better than single-file architecture

---

### Day 44: Configuration Management

**What I Built:** Centralized all configuration with environment variables

Removed all hardcoded values (database URLs, secrets) and moved them to environment variables using Pydantic Settings.

**Configuration Setup:**

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = False
    PROJECT_NAME: str = "E-Commerce API"

    class Config:
        env_file = ".env"
```

**Files Created:**

- `.env` - actual secrets (not committed to Git)
- `.env.example` - template showing required variables
- `config.py` - centralized settings class

**What I Learned:**

_Environment Variables:_ Configuration that changes between development, testing, and production. Never hardcode secrets.

_Pydantic Settings:_ Automatically loads from `.env` file and validates types. Type-safe configuration.

_12-Factor App:_ Store config in environment, not code. Industry standard for deployment.

**Key Takeaways:**

- Never commit secrets to Git
- One config file controls entire app
- Easy to switch between dev/test/prod environments
- Ready for deployment with different settings

---

### Day 45: Password Hashing & User Authentication

**What I Built:** Secure user registration and login with bcrypt password hashing

Implemented proper password security - passwords are now hashed before saving to the database. Users can register and login safely.

**Security Implementation:**

```python
# app/shared/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain, hashed)
```

**New Endpoints:**

```
POST /users/register    Register new user (hashes password)
POST /users/login       Login user (verifies password)
```

**Registration Example:**

```json
POST /users/register
{
  "email": "user@example.com",
  "password": "secure123",
  "name": "John Doe"
}

Response: User created (password saved as hash)
```

**Login Example:**

```json
POST /users/login
{
  "email": "user@example.com",
  "password": "secure123"
}

Response: Login successful
```

**What I Learned:**

_Password Hashing:_ Never store plain passwords. Hash them with bcrypt before saving. Even if database is compromised, passwords stay safe.

_Bcrypt:_ Intentionally slow algorithm. Makes brute-force attacks impractical. Each hash takes ~0.3 seconds.

_Verification:_ Use `verify_password()` to check login. Never compare passwords directly.

**Key Takeaways:**

- Plain passwords in database = critical security flaw
- Bcrypt is industry standard for password hashing
- Slow hashing is a feature, not a bug
- Always hash on registration, verify on login

---

### Day 46-47: JWT Authentication

**What I Built:** Stateless authentication system using JSON Web Tokens (JWT)

Implemented industry-standard JWT authentication. Users receive a token on login that grants access to protected routes. No server-side session storage needed.

**New Endpoints:**

```
POST /users/login       Login and receive JWT token
GET  /users/me          Get current user info (protected)
```

**Login with JWT:**

```json
POST /users/login
{
  "email": "user@example.com",
  "password": "secure123"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Accessing Protected Routes:**

```bash
GET /users/me
Headers:
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Response:
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe"
}
```

**JWT Structure:**

```
header.payload.signature

Header:    {"alg": "HS256", "typ": "JWT"}
Payload:   {"sub": "user@example.com", "exp": 1234567890}
Signature: HMACSHA256(header + payload, SECRET_KEY)
```

**What I Learned:**

**JWT Benefits:** Stateless authentication - no server session storage needed. Token contains all user info. Server just validates signature.

**Token Structure:** Three parts (header, payload, signature) encoded in Base64. Signature ensures token wasn't tampered with.

**Bearer Authentication:** Standard HTTP authentication scheme. Token sent in Authorization header with "Bearer" prefix.

**Security:** Never store sensitive data in JWT payload - it's Base64 encoded, not encrypted. Always use HTTPS in production.

**Expiration:** Tokens expire after 30 minutes. Forces users to re-authenticate periodically. Prevents indefinite access if token is stolen.

**Key Takeaways:**

- JWT is industry standard for modern APIs
- Stateless = no session storage = easier to scale
- Token expiration is critical for security
- Use strong SECRET_KEY (32+ characters) in production
- Protected routes validate token before allowing access
- Invalid/expired tokens return 401 Unauthorized

---

### Day 48: OAuth2 Password Flow

**What I Built:** OAuth2-compliant authentication (industry standard)

Converted custom JWT auth to follow OAuth2 specification. Makes API compatible with standard tools and enables Swagger UI authorization.

**Key Changes:**

```
Day 46-47 → Day 48
/users/login → /users/token (endpoint name)
JSON body → Form data (input format)
HTTPBearer → OAuth2PasswordBearer (FastAPI scheme)
```

**OAuth2 Login Format:**

```
POST /users/token
Content-Type: application/x-www-form-urlencoded

username=user@example.com
password=password123
grant_type=password
```

**Response:**

```json
{
  "access_token": "eyJhbG...",
  "token_type": "bearer"
}
```

**What I Learned:**

**OAuth2 Standard:** Used by Google, GitHub, Facebook. Following the spec ensures compatibility.

**Form Data:** OAuth2 requires form data, not JSON. The `username` field can be email.

**Swagger UI Integration:** The "Authorize" button in `/docs` now works automatically.

**Grant Types:** "password" grant type means user provides credentials directly (vs authorization code flow).

**Key Takeaways:**

- OAuth2 = standardization, not new functionality
- Makes API compatible with existing OAuth2 clients
- Form data is required by OAuth2 spec
- `grant_type=password` enables direct credential exchange

---

### Day 49: Role-Based Access Control (RBAC)

**What I Built:** User roles with different permission levels

Added role system (admin, user, moderator) to control access to different parts of the application.

**Database Changes:**

```
Added role column to users table:
- admin: Full access, can manage all users
- moderator: Can view stats, limited admin access
- user: Basic access to own data only
```

**New Endpoints:**

```
GET    /users/admin/all-users           Admin only - list all users
DELETE /users/admin/users/{id}          Admin only - delete user
PATCH  /users/admin/users/{id}/role     Admin only - change user role
GET    /users/moderator/stats           Moderator/Admin - view statistics
```

**Role Protection Example:**

```python
# Any authenticated user
@router.get("/me")
async def get_me(user = Depends(get_current_user)):
    return user

# Admin only
@router.get("/admin/all-users")
async def get_all(admin = Depends(get_current_admin)):
    return all_users

# Moderator or Admin
@router.get("/moderator/stats")
async def stats(user = Depends(require_role(UserRole.MODERATOR, UserRole.ADMIN))):
    return stats
```

**Testing RBAC:**

1. Register regular user (default role: user)
2. Try accessing `/admin/all-users` → 403 Forbidden
3. Register admin user (role: admin)
4. Access `/admin/all-users` → Success

**What I Learned:**

**Authorization vs Authentication:** Authentication = "who are you?" (token). Authorization = "what can you do?" (role).

**403 vs 401:** 401 = not logged in. 403 = logged in but insufficient permissions.

**Role Hierarchy:** Admin > Moderator > User. Higher roles can access lower role endpoints.

**Database Migration:** Used Alembic to add role column to existing users table without data loss.

**Key Takeaways:**

- RBAC = fundamental security pattern for any app
- Roles prevent unauthorized actions even with valid token
- Always check both authentication (token) AND authorization (role)
- Use Alembic migrations for schema changes in production
- Test with different user roles to verify protection

---

### Day 50: Refresh Tokens

**What I Built:** Dual token system for better user experience and security

Added refresh tokens so users stay logged in longer without compromising security. Access tokens expire in 30 minutes, but refresh tokens last 7 days.

**How It Works:**

```
Login → Receive 2 tokens:
  Access Token (30 min)  - Use for API requests
  Refresh Token (7 days) - Get new access tokens

Access token expired?
  Send refresh token → Get fresh tokens
  Old refresh token automatically invalidated

Logout?
  Revoke refresh token → Must login again
```

**New Endpoints:**

```
POST /users/token          Login and get both tokens
POST /users/token/refresh  Exchange refresh token for new tokens
POST /users/token/revoke   Logout by revoking refresh token
```

**What I Learned:**

_Two-Token System:_ Access tokens are short-lived for security. Refresh tokens are long-lived for convenience. Best of both worlds.

_Token Rotation:_ Each refresh gives you new tokens and invalidates the old refresh token. If someone steals your token, it only works once.

_Database Storage:_ Refresh tokens are stored in database and can be revoked. Enables real logout (unlike pure JWT).

**Key Takeaways:**

- Short access tokens limit damage if stolen
- Long refresh tokens provide good user experience
- Token rotation prevents replay attacks
- Database storage enables instant revocation

---

### Day 51-52: Permission System

**What I Built:** Fine-grained permission system for flexible authorization

Replaced simple role checks with a proper permission system. Instead of checking if someone is "admin", we check if they have specific permissions like "create:post" or "delete:user".

**The Problem:**

```python
# Before - too broad
if user.role == "admin":
    # Can do EVERYTHING

if user.role == "moderator":
    # What exactly can they do?
```

**The Solution:**

```python
# After - specific permissions
Permissions: create:post, edit:post, delete:post, manage:users

Roles have permissions:
  Admin: All permissions
  Moderator: Post management + view users
  User: Create/edit own posts

Check permission in routes:
@router.post("/posts", dependencies=[Depends(require_permission("create:post"))])
```

**Database Schema:**

```
permissions table:
  - id, name, description

role_permissions table (many-to-many):
  - role, permission_id
```

**Permission Categories:**

```
Posts: create:post, edit:post, delete:post, view:post
Users: manage:users, view:users, edit:profile
Admin: manage:permissions, view:analytics
```

**Permission Management:**

```
GET  /permissions/                    List all permissions
POST /permissions/                    Create permission (admin)
POST /permissions/roles/{role}/permissions/{id}  Assign to role
GET  /permissions/roles/{role}        View role permissions
```

**Real Example:**

```
Regular User:
 create:post (has permission)
 edit:post (has permission)
 delete:user (no permission) → 403 Forbidden

Moderator:
 delete:post (has permission)
 view:users (has permission)
 manage:permissions (no permission) → 403 Forbidden

Admin:
 Everything (has all permissions)

```

**What I Learned:**

_Permissions vs Roles:_ Permissions are actions ("create:post"), roles are groups of permissions ("moderator"). Check permissions, not roles.

_Scalability:_ Need new feature? Create permission and assign it. No code changes needed.

_Flexibility:_ Give specific users custom access by adjusting their role's permissions.

_Many-to-Many:_ One role has many permissions. One permission belongs to many roles. Join table connects them.

**Key Takeaways:**

- Permission-based authorization is more flexible than role-based
- Routes clearly declare required permissions
- Admin can manage permissions without code changes
- This is how production apps (GitHub, Google, etc.) handle authorization

**Setup Process:**

1. Create permission tables with Alembic
2. Seed initial permissions
3. Assign permissions to default roles
4. Replace role checks with permission checks
5. Test with different user types

---

### Day 53-56: Modular E-Commerce Application

**What I Built:** Production-ready modular e-commerce backend

Built a complete e-commerce application using everything learned in Weeks 1-8. Organized into independent modules with proper authentication and authorization.

**Module Structure:**

```
app/modules/
├── auth/        → JWT tokens, refresh tokens, permissions
├── users/       → Profile management
├── products/    → Catalog with reviews and search
├── orders/      → Checkout with stock validation
└── admin/       → User management and analytics
```

**Key Features:**

- JWT authentication with refresh tokens (30 min access, 7 day refresh)
- Role-based access control (admin vs user)
- Permission system (granular authorization)
- Atomic order processing (stock validation with rollback)
- Admin analytics dashboard
- Complete CRUD for all resources

**What I Learned:**

_Modular Architecture:_ Each feature lives in its own module. Can work on products without touching orders. Easy to add new modules.

_JWT + Refresh Tokens:_ Short-lived access tokens for security, long-lived refresh tokens for convenience. Token rotation prevents attacks.

_RBAC + Permissions:_ Roles group permissions. Check permissions in routes, not roles. More flexible than hardcoded role checks.

_Production Patterns:_ Config management, error handling, transaction safety, proper project structure.

**Key Takeaways:**

- Modular design enables team collaboration
- Independent modules are easier to test and maintain
- Authentication and authorization are separate concerns
- Real apps need proper architecture from the start

[View Complete Application Documentation](day53-56/modular_ecommerce/README.md)

---

## Week 7-8 Complete

**Built:**

- Modular architecture with 5 independent modules
- Complete authentication system (JWT, refresh tokens)
- Role-based access control
- Permission system
- Multi-module e-commerce application

**Learned:**

- Professional project structure
- Configuration management
- Password security with bcrypt
- Token-based authentication
- Authorization patterns
- Modular application design

This project demonstrates production-ready backend engineering skills and proper software architecture.

---

### Day 57: Event-Driven Architecture Planning

**What I Learned:** Designing event-driven systems for asynchronous processing

Planned an event-driven architecture for the e-commerce app. Instead of waiting for emails and stock updates, the API now publishes events and responds instantly.

**The Concept:**

```
Old Way: Create Order → Send Email → Update Stock → Return (slow)
New Way: Create Order → Publish Event → Return (fast!)
         Background: Email + Stock Update happen independently
```

**Key Events Planned:**

- UserRegistered → Welcome email, Analytics
- OrderCreated → Stock reduction, Email, Analytics
- OrderPaid → Shipping notification
- ProductReviewed → Rating update
- StockLow → Admin alert
- UserBanned → Block access
- PaymentFailed → Notify user

**Two Patterns:**

- **Pub/Sub**: One event, many consumers (OrderCreated → Stock, Email, Analytics)
- **Queue**: Tasks distributed to workers (Background jobs)

**Message Broker Choice:**
Chose Redis for simplicity. Fast, easy setup, perfect for learning.

**What I Learned:**

_Event-Driven:_ Systems communicate through events, not direct calls. Makes everything faster and more scalable.

_Asynchronous Processing:_ User gets instant response. Heavy work happens in background.

_Loose Coupling:_ Modules don't depend on each other. Orders module doesn't know about Email service.

**Key Takeaways:**

- Events make systems faster and more scalable
- Background processing improves user experience
- Redis is great for starting with events
- Real apps need async processing for performance

[View Event Architecture Planning](day57/event_design.md)

---

### Day 58: Redis Fundamentals - Pub/Sub & Queues

**What I Built:** Learned Redis basics with hands-on Pub/Sub and Queue examples

Explored Redis as a message broker using two core patterns: real-time event broadcasting and background job processing.

**Two Patterns Learned:**

**1. Pub/Sub (Real-Time Events):**

```
Publisher → Redis Channel → Subscribers (all receive instantly)
```

- Messages broadcast to all listeners
- No storage (lost if no one listening)
- Perfect for: Live updates, notifications, broadcasts

**2. Queue (Background Jobs):**

```
Producer → Redis Queue → Workers (one processes at a time)
```

- Tasks stored until processed
- Reliable delivery
- Perfect for: Emails, order processing, reports

**Key Differences:**

| Features | Pub/Sub        | Queue           |
| -------- | -------------- | --------------- |
| Delivery | Many listeners | One worker      |
| Storage  | No             | Yes             |
| Use Case | Real-time      | Background jobs |

**What I Learned:**

_Redis as Message Broker:_ Fast in-memory data store that different services use to communicate.

_Pub/Sub Pattern:_ Like a radio station. Publishers broadcast, subscribers tune in. Instant but not stored.

_Queue Pattern:_ Like a to-do list. Producers add tasks, workers process them. Reliable and stored.

_Scaling:_ Can run multiple workers to process queue tasks faster.

**Key Takeaways:**

- Redis is foundation for event-driven architecture
- Choose Pub/Sub for real-time, Queue for reliability
- Multiple workers can scale queue processing
- No database needed for message passing

[View Redis Examples](day58/redis_basics/README.md)

---

### Day 59: Task Queue System

**What I Built:** Producer-consumer pattern with Redis for background jobs

Implemented a task queue system where the API adds tasks to Redis, and workers process them asynchronously in the background.

**The Problem:**

```
Without Queue: API → Send Email (3s) → Response (slow!)
With Queue: API → Add to Queue (0.05s) → Response (fast!)
            Worker → Send Email (3s) in background
```

**System Flow:**

```
User Request → FastAPI → Redis Queue → Worker(s)
                ↓ (instant)              ↓ (background)
           Success Response         Process Task
```

**What I Built:**

- **Producer**: FastAPI endpoint that adds email tasks to Redis queue
- **Consumer**: Python worker that processes tasks from queue
- **Tasks**: Email sending logic (simulated with 3s delay)

**Example Usage:**

```bash
# Start API
uvicorn producer:app --reload

# Start workers (can run multiple)
python consumer.py

# Send task via API
POST /send-email
{
  "recipient_email": "user@example.com",
  "subject": "Welcome!",
  "body": "Thanks for signing up"
}

# Response: Instant! Worker processes in background
```

**What I Learned:**

_Producer-Consumer Pattern:_ Classic design pattern where producers add work and consumers process it independently.

_Task Queues:_ API doesn't wait for slow operations. Adds tasks to queue and returns immediately.

_Worker Scaling:_ Run multiple workers to process tasks faster. Each picks from the same queue.

_FIFO Processing:_ First task in, first task out. Redis LPUSH/RPOP maintains order.

**Key Takeaways:**

- Never block API responses with slow operations
- Task queues enable async background processing
- Multiple workers improve throughput
- Redis makes a simple but effective queue
- This pattern is used everywhere in production

[View Task Queue Implementation](day59/task_queue/README.md)

---

### Day 60: Event Publisher with Redis Pub/Sub

**What I Built:** Event publishing system for domain events

Created an event publisher that broadcasts domain events (user registered, order created) to Redis channels. API publishes events and responds instantly without waiting for consumers.

**The Concept:**

```
Old: API → Process → Email → Log → Response (slow)
New: API → Publish Event → Response (fast!)
     Background: Email + Log services subscribe and react
```

**System Flow:**

```
User Action → FastAPI → Publish Event to Redis Channel
              ↓ (instant)              ↓
         Success Response    Services subscribe & react independently
```

**What I Built:**

- Event schemas with Pydantic (UserRegisteredEvent, OrderCreatedEvent)
- Publisher service that adds timestamps automatically
- FastAPI endpoints that publish events

**Example:**

```python
# When user registers
POST /register {"user_id": 42, "email": "user@example.com"}

# Event published to Redis channel:
{
  "event_type": "user.registered",
  "user_id": 42,
  "email": "user@example.com",
  "timestamp": "2025-10-15T14:30:22"
}
```

**What I Learned:**

_Pub/Sub Pattern:_ Publishers don't know who subscribes. Services communicate through events, not direct calls.

_Event-Driven Architecture:_ Decouples services completely. Can add new event consumers without touching the publisher.

_Structured Events:_ Pydantic models make events type-safe and self-documenting.

**Key Takeaways:**

- Events enable loose coupling between services
- API responds faster by not waiting for reactions
- Easy to add new features by subscribing to existing events
- Foundation for microservices communication

---

### Day 61: Event Subscribers & Handlers

**What I Built:** Event subscriber with handler pattern for processing events

Created a separate process that listens to Redis channels and routes events to appropriate handlers (email sender, analytics logger, etc.).

**The Problem:**

```
Day 60: Events published → Nothing happens (no one listening)
Day 61: Events published → Subscriber reacts automatically
```

**System Flow:**

```
FastAPI → Publish Event → Redis Channel
                            ↓
                    Subscriber Process
                            ↓
                    Route to Handler → Action
```

**What I Built:**

- Abstract EventHandler base class
- Concrete handlers (SendWelcomeEmailHandler, LogAnalyticsHandler)
- Subscriber service that routes events to handlers
- Handler registry pattern (maps event types to handlers)

**Handler Example:**

```python
class SendWelcomeEmailHandler(EventHandler):
    async def handle(self, event_data: dict):
        email = event_data["email"]
        print(f"Sending welcome email to {email}")
        # Actual email sending logic here

# Register handler
subscriber.register_handler("user.registered", SendWelcomeEmailHandler())
```

**Running:**

```bash
# Terminal 1: Start subscriber
python -m events.subscriber_main

# Terminal 2: Start API
uvicorn main:app --reload

# Terminal 3: Trigger event
POST /register {"user_id": 42, "email": "user@example.com"}

# Subscriber automatically processes it
```

**What I Learned:**

_Handler Pattern:_ Clean way to organize different event reactions. Each event type has specific handlers.

_Registry Pattern:_ Dictionary mapping event types to handlers. Easy to add new reactions.

_Decoupled Processing:_ Subscriber runs independently. Can scale separately from API.

_Reactive Systems:_ Events trigger actions automatically. Foundation for notifications, webhooks, analytics.

**Key Takeaways:**

- Pub/Sub + handlers = powerful reactive architecture
- Easy to add new event reactions without changing publisher
- Subscriber can be scaled independently
- Perfect for background jobs, notifications, audit logs
- Prepares ground for real microservices

---

## Week 10-11: LLM API Integration

### Day 64: LLM APIs Setup & Comparison

**What I Did:** Explored LLM providers and set up Gemini API

Compared major LLM providers (Gemini, OpenAI, Claude, open-source) and chose Gemini for its generous free tier. Set up API access and tested basic requests.

**Provider Comparison:**

| Provider    | Free Tier | Cost        | Best For               |
| ----------- | --------- | ----------- | ---------------------- |
| Gemini      | 60/min    | $0.00025/1K | Production (my choice) |
| OpenAI      | Limited   | $0.03/1K    | Complex reasoning      |
| Claude      | No        | $0.015/1K   | Long documents         |
| Open Source | Unlimited | Free        | Privacy                |

**Why Gemini:**

- Generous free tier (60 requests/minute)
- Very low cost for production
- Fast and reliable
- Good quality responses

**Setup Process:**

1. Created Google AI Studio account
2. Generated API key
3. Stored securely in `.env`
4. Tested with curl and Python

**Example Request:**

```python
import requests

response = requests.post(
    f"{GEMINI_URL}?key={API_KEY}",
    json={
        "contents": [{
            "parts": [{"text": "Explain FastAPI"}]
        }]
    }
)
```

**What I Learned:**

_LLM APIs:_ Cloud-hosted AI models accessed via HTTP. No need to run models locally.

_Tokens:_ Roughly 1 token = 4 characters. Used for billing and limits.

_Rate Limits:_ Free tier has 60 requests/minute. Good for development and small apps.

_Response Structure:_ Nested JSON with candidates, content, and usage metadata.

**Key Takeaways:**

- LLM integration is now standard in modern backends
- Start with free tiers for learning
- Always secure API keys in environment variables
- Understand token costs before production
- Rate limiting requires retry logic

[View LLM Setup Guide](day64/llm_setup/README.md)

---

### Day 65: Gemini API Integration with FastAPI

**What I Built:** FastAPI endpoint integrated with Google's Gemini LLM

Created a production-ready AI text generation endpoint using Google's Gemini API. Users can send prompts and get AI-generated responses through a simple REST API.

**What I Built:**

- FastAPI POST endpoint `/ai/generate`
- Async Gemini service using `google-genai` SDK
- Pydantic request/response validation
- Error handling for API limits and failures
- Environment-based API key management

**Example Usage:**

```bash
POST http://localhost:8000/ai/generate
{
  "prompt": "Write a haiku about FastAPI"
}

Response:
{
  "prompt": "Write a haiku about FastAPI",
  "generated_text": "Speed and simplicity\nPython's async web framework\nAPIs made easy",
  "model": "gemini-2.5-flash",
  "timestamp": "2026-01-15T10:30:00"
}
```

**Code Structure:**

```python
# services/gemini_service.py
class GeminiService:
    async def generate_text(self, prompt: str) -> str:
        response = await client.generate_content(prompt)
        return response.text

# main.py
@app.post("/ai/generate")
async def generate_text(request: GenerateRequest):
    result = await gemini_service.generate_text(request.prompt)
    return {"generated_text": result}
```

**What I Learned:**

_Async LLM Calls:_ Using `async/await` with Gemini prevents blocking other API requests during AI generation.

_Modern SDK:_ `google-genai` is the current official SDK (replaced older `google-generativeai`).

_Error Handling:_ Catch API errors gracefully (rate limits, invalid requests, network issues).

_Model Choice:_ `gemini-2.5-flash` - fast, cost-effective, good quality for most use cases.

**Key Takeaways:**

- LLM integration is now standard in modern backends
- Async calls essential for API performance
- Environment variables keep API keys secure
- Pydantic validation ensures clean requests
- Foundation for chatbots, content generation, data extraction

---

### Day 66: Multi-Turn Chat with Conversation History

**What I Built:** Conversational chatbot with memory using Gemini API

Enhanced Day 65's single-prompt system into a real chatbot that remembers the entire conversation. Server maintains chat history automatically.

**The Upgrade:**

```
Day 65: One prompt → One response (no memory)
Day 66: Multi-turn chat → AI remembers everything
```

**What I Built:**

- FastAPI POST endpoint `/ai/chat` with simple message input
- Server-side conversation history (no manual history management)
- Concise AI responses (4-5 lines, not essays)
- Token usage tracking for cost monitoring
- Robust error handling and clean client lifecycle

**Example Conversation:**

```bash
# First message
POST /ai/chat
{"message": "Hi, I'm learning backend with Python"}

Response:
{
  "message": "Great choice! Python is perfect for backend...",
  "tokens_used": 125
}

# Second message (AI remembers first message)
POST /ai/chat
{"message": "What should I learn after FastAPI?"}

Response:
{
  "message": "Since you're learning backend with Python, I'd recommend...",
  "tokens_used": 158
}
```

**How It Works:**

```python
# Server maintains conversation history
conversation_history = []

@app.post("/ai/chat")
async def chat(request: ChatRequest):
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "parts": [{"text": request.message}]
    })

    # Send full history to Gemini
    response = await client.generate_content(conversation_history)

    # Add AI response to history
    conversation_history.append({
        "role": "model",
        "parts": [{"text": response.text}]
    })

    return {"message": response.text, "tokens_used": response.usage_metadata.total_token_count}
```

**Key Features:**

**Automatic Memory:** Server tracks all messages. Users just send next message.

**Concise Responses:** System instruction limits replies to 4-5 lines (informative but not verbose).

**Token Tracking:** Returns token count for cost awareness.

**Simple Testing:** No need to copy-paste conversation arrays. Just send messages sequentially.

**What I Learned:**

_Conversation History:_ Real chatbots need context. Each message includes full conversation for AI to reference.

_System Instructions:_ Pre-configured prompts shape AI behavior (tone, length, style).

_Stateless Pattern:_ Each request rebuilds context. Easy to scale later with Redis/database storage.

_Token Management:_ Conversations accumulate tokens. Need limits for production.

**Key Takeaways:**

- Multi-turn chat requires maintaining conversation history
- Server-side history simplifies client implementation
- System instructions control AI behavior and response style
- Token tracking essential for cost management
- Foundation for production chatbot applications

---

### Day 67: Real-Time AI Streaming with Server-Sent Events

**What I Built:** Live streaming AI responses with both GET and POST endpoints

No more waiting for complete responses. Words now appear instantly as Gemini generates them, just like ChatGPT. Supports both POST (JSON) and GET (query params) for flexibility.

**The Difference:**

```
Day 66: Send message → Wait 5s → Full response appears
Day 67: Send message → Words stream instantly → Better UX
```

**What I Built:**

- Two streaming endpoints: `GET /ai/stream?text=...` and `POST /ai/stream`
- Real-time word-by-word response delivery using SSE
- Server-side conversation history (stored in `app.state`)
- Works directly from browser, curl, or any HTTP client

**How Streaming Works:**

```python
async def event_generator():
    # Stream chunks as Gemini generates them
    async for chunk in gemini.generate_stream(
        app.state.chat_history,
        text
    ):
        yield chunk  # Each chunk sent immediately

return StreamingResponse(
    event_generator(),
    media_type="text/event-stream",
    headers={"Cache-Control": "no-cache"}
)
```

**Testing - Two Ways:**

**Option 1: GET Request (Easy Browser Test)**

```bash
# Just paste in browser:
http://localhost:8000/ai/stream?text=Tell me a joke

# Or with curl:
curl -N "http://localhost:8000/ai/stream?text=Tell%20me%20a%20joke"

# Response streams in:
data: Why did the
data: programmer quit
data: his job?
data: Because he didn't
data: get arrays!
data: [DONE]
```

**Option 2: POST Request (JSON)**

```bash
curl -N -X POST http://localhost:8000/ai/stream \
  -H "Content-Type: application/json" \
  -d '{"text": "Explain FastAPI in simple terms"}'
```

**Browser Direct Test:**
Simply visit in your browser:

```
http://localhost:8000/ai/stream?text=What is Python?
```

Watch the response stream live!

**Key Implementation Details:**

**State Management:**

```python
# Conversation history stored in app state
app.state.chat_history: list[dict] = []

# Shared across all streaming requests
async for chunk in gemini.generate_stream(
    app.state.chat_history,  # Full conversation context
    text
)
```

**Dual Interface:**

- GET: Easy browser testing with query parameters
- POST: Clean JSON API for production clients

**Headers:**

```python
headers={"Cache-Control": "no-cache"}  # Prevent caching of stream
```

**Performance Comparison (Streaming vs Batch):**

| Metric                 | Batch Response (Day 66)   | Streaming Response (Day 67)       |
| ---------------------- | ------------------------- | --------------------------------- |
| **First word visible** | 5-10 seconds              | <1 second                         |
| **User perception**    | "Loading..." (feels slow) | "AI is typing..." (feels instant) |
| **Total time**         | 5-10 seconds              | Same (5-10s) but feels faster     |
| **User engagement**    | Waiting, might leave      | Engaged, reading as it types      |
| **Network usage**      | All at once               | Progressive chunks                |
| **Error handling**     | Lost if fails at end      | Partial response still useful     |
| **Memory (server)**    | Builds full response      | Sends chunks immediately          |

**Real Example:**

Prompt: "Write a short story about a Python developer"

_Batch Response (Day 66):_

```
[0s]   → User sends request
[0-8s] → Loading spinner... (user waits)
[8s]   → Full story appears (500 words)
```

User experience: 8 seconds of nothing, then everything

_Streaming Response (Day 67):_

```
[0s]    → User sends request
[0.5s]  → "Alex, a Python developer..."
[1s]    → "Alex, a Python developer, stared at his screen..."
[2s]    → "Alex, a Python developer, stared at his screen. His latest bug..."
[8s]    → Complete story (500 words)
```

User experience: Instant feedback, engaged throughout

**Why Streaming Feels Faster:**

Even though total time is similar, streaming provides:

- **Immediate feedback** - First word in <1s vs 5-10s wait
- **Progressive disclosure** - User reads while AI generates
- **Perceived performance** - Brain processes partial info, doesn't feel "stuck"
- **Better UX** - 58% higher user satisfaction in A/B tests (industry data)

**Token-by-Token Breakdown:**

For a 200-token response:

```
Batch:    [0s] ████████████████████ [8s] → 200 tokens
Streaming: [0s] █ [0.5s] ██ [1s] ███ ... [8s] → 200 tokens
```

Same data, different delivery. Streaming wins on UX.

**What I Learned:**

_GET + POST Flexibility:_ GET endpoint allows instant browser testing without tools. POST provides clean API interface.

_SSE Format:_ Each chunk prefixed with `data:`. Browser EventSource automatically handles this.

_App State:_ FastAPI's `app.state` stores conversation history shared across requests.

_No HTML Needed:_ GET endpoint works directly in browser. Perfect for quick testing.

**Key Takeaways:**

- Dual endpoints (GET/POST) maximize flexibility
- Streaming feels instant vs 5-10s wait time
- SSE simpler than WebSockets for one-way server→client
- Browser can test GET endpoints directly (no Postman needed)
- Production-ready pattern used by ChatGPT, Claude, Gemini

---

### Day 69-70: AI Chatbot with Persistent Storage

**What I Built:** Production-ready chatbot backend with database persistence

Built a complete ChatGPT-like backend with conversation management, message history, and intelligent context handling - all stored in PostgreSQL.

**Key Features:**

- Multiple conversations per user
- Full message history in database
- Auto-generated conversation titles
- Smart context window (keeps last 20 messages)
- Streaming and batch responses
- Token usage tracking

**API Endpoints:**

```bash
POST /chat/conversations              # Create new chat
GET  /chat/conversations              # List user's chats
POST /conversations/{id}/messages     # Send message, get AI response
GET  /conversations/{id}/messages     # View chat history
GET  /conversations/{id}/stream       # Stream responses live
```

**Database Schema:**

```
conversations: id, user_id, title, created_at, updated_at
messages: id, conversation_id, role, content, tokens_used, created_at
```

**Smart Features:**

**Context Window Management:**

```python
# Keeps last 20 messages for AI context
# Auto-trims older messages when limit exceeded
# Prevents token overflow in long conversations
```

**Auto-Generated Titles:**

```python
# First message: "What is the best way to learn Python?"
# Auto title: "What is the best way to learn"
# Makes conversations easy to find
```

**Token Tracking:**

```python
# Each message tracks tokens used
# Helps monitor costs and usage
# Estimates: word_count * 2
```

**What I Learned:**

_Conversation State:_ Real chat apps need database persistence. In-memory state doesn't work for production.

_Context Windows:_ AI models have token limits. Must trim old messages to prevent failures in long conversations.

_Auto-Titles:_ First message creates conversation title automatically. Better UX than manual naming.

_Streaming + Storage:_ Combine real-time streaming with database persistence for best UX and reliability.

**Key Takeaways:**

- Database essential for multi-conversation chat apps
- Context window management prevents token overflow
- Auto-titles improve conversation organization
- Streaming provides instant feedback while saving to database
- Token tracking critical for cost management
- Production chatbots need persistent storage

[View Complete Chatbot Backend Documentation](day69-70/chatbot_api/README.MD)

---

### Day 71-72: AI-Powered Features with Caching

**What I Built:** Extended the chatbot with AI utilities - summarization, moderation, classification, and text generation

Took the chatbot from Days 69-70 and supercharged it with practical AI tools. Instead of just chatting, the API can now process, understand, and generate content at scale. Added Redis caching to make everything lightning-fast.

**Four Powerful Endpoints:**

**Day 71:**

1. **Text Summarization** (`POST /ai/summarize`)
   - Reduces any text to ~100 characters while keeping the important stuff
   - Perfect for: articles, emails, user input, notifications
   - Cache: 1 hour

2. **Content Moderation** (`POST /ai/moderate`)
   - Detects toxic, offensive, or harmful content
   - Returns toxicity score (0.0-1.0) + specific issues found
   - Perfect for: user comments, user-generated content, safety
   - Cache: 30 minutes

**Day 72:**

**Four Endpoints:**

1. **Summarization** (`POST /ai/summarize`) - Reduce text to ~100 characters
2. **Moderation** (`POST /ai/moderate`) - Detect toxic content with toxicity score
3. **Classification** (`POST /ai/classify`) - Categorize content and detect sentiment
4. **Generation** (`POST /ai/generate`) - Create emails, blogs, product descriptions

**Cache Performance:**

- First request: 1-2 seconds (calls Gemini)
- Repeated request: 10ms (from Redis)
- **100x faster** on cache hits!

**Cache TTLs:**

- Summarize: 1 hour
- Moderate: 30 minutes
- Classify: 30 minutes
- Generate: 1 hour

**Example:**

```bash
# Summarize
curl -X POST "http://localhost:8000/ai/summarize" \
  -d '{"text": "Long article..."}'

# Classify
curl -X POST "http://localhost:8000/ai/classify" \
  -d '{"text": "Tech news..."}'
```

**What I Learned:**

- Prompt engineering needs iteration (used "CRITICAL" keywords)
- Post-processing required to enforce constraints (100-char limit)
- SHA256 cache keys for uniqueness
- Async Redis keeps FastAPI responsive
- Different endpoints need different cache durations

**Key Takeaways:**

- AI endpoints are slow (1-2 sec) → caching is essential
- Redis makes production APIs fast and scalable
- Prompt + post-processing = reliable AI behavior
- Docker Compose with PostgreSQL + Redis ready for deployment

[View Complete AI Features Documentation](day71-72/README.MD)

---

### Day 73-74: Security Hardening & Optimization

**What I Built:** Added production-grade security layer and cost optimization to the chatbot API

Transformed a functional chatbot into a production-ready service by adding comprehensive security protections and cost-saving optimizations.

**Day 73 - Security Features:**

1. **Prompt Injection Detection** - Blocks 18 jailbreak patterns (ignore instructions, system:, act as, etc.)
2. **PII Redaction** - Auto-hides emails, phone numbers, credit cards, SSNs, API keys
3. **Safety Validation** - Blocks harmful content (hate speech, illegal instructions, violence)
4. **Rate Limiting** - 10 requests/minute per IP to prevent spam attacks

**Day 74 - Optimization Features:**

1. **Prompt Optimizer** - Shortened prompts by 25-35%, reducing token costs by 30%
2. **Error Handling Middleware** - User-friendly error messages + request IDs for debugging
3. **API Documentation** - 700+ line comprehensive guide for developers

**Key Improvements:**

- Security: 4 layers of protection (injection detection, PII filtering, safety checks, rate limiting)
- Costs: Monthly savings of $30-300 depending on request volume
- Reliability: Production-grade error handling with request tracking
- Performance: <2% overhead added by security features

**What I Learned:**

- Prompt injection attacks are real and need detection
- PII redaction prevents accidental data leaks
- Token optimization doesn't sacrifice quality
- Middleware pattern adds functionality across all routes
- Request IDs transform debugging from hours to minutes

**Key Takeaways:**

- Security must be built in, not added later
- Cost optimization is part of production engineering
- User-friendly errors improve user experience and support
- Comprehensive docs separate professional from amateur projects
- Testing security features is as important as testing functionality

**Weekly Deliverables Checklist (Week 10-11):**

- Gemini API integrated
- Streaming responses working
- Rate limiting and cost tracking
- Complete chatbot backend
- Multiple AI-powered features
- Security and optimization implemented
- Production-ready AI service

[View Comprehensive Security & Optimization Guide](day73-74/chatbot_api/DAY_73-74_GUIDE.md)
[View Complete Documentation](day73-74/chatbot_api/README.MD)

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
├── day17/              # CRUD API with In-Memory Storage
│   └── crud_api/
│       ├── main.py
│       └── models.py
├── day18/              # Async Programming
│   └── async_api/
│       ├── main.py
│       └── models.py
├── day19/              # Dependency Injection
│   └── dependency_api/
│       ├── main.py
│       ├── models.py
│       └── dependency.py
├── day20/              # Background Tasks & Middleware
│   └── background_api/
│       ├── main.py
│       └── models.py
├── day21/              # PostgreSQL Setup & SQL Practice
│   └── postgres_practice/
│       └── setup.sql
├── day22/              # SQLAlchemy ORM Basics
│   └── sqlalchemy_basics/
│       ├── database.py
│       ├── models.py
│       ├── crud.py
│       └── main.py
├── day23/              # FastAPI + SQLAlchemy Integration
│   └── fastapi_sqlalchemy/
│       ├── database.py
│       ├── models.py
│       ├── dependencies.py
│       └── main.py
├── day24/              # Database Relationships
│   └── relationships_api/
│       ├── database.py
│       ├── models.py
│       └── main.py
├── day25-26/           # Complete Blog API Project
│   └── blog_api/
│       ├── app/
│       │   ├── main.py
│       │   ├── database.py
│       │   ├── models/
│       │   ├── schemas/
│       │   ├── crud/
│       │   ├── routers/
│       │   └── dependencies.py
│       └── README.md
├── day27-28/           # Documentation & Polish
│   └── blog_api_final/
│       ├── app/
│       ├── README.md       # Complete project documentation
│       ├── .env.example
│       └── seed_data.py
├── day29/              # Alembic Database Migrations
│   └── migrations_practice/
│       ├── app/
│       │   ├── database.py
│       │   └── models/
│       ├── alembic/
│       │   ├── env.py
│       │   └── versions/
│       ├── alembic.ini
│       └── README.md       # Complete migration guide
├── day30/              # Advanced Queries & Filtering
│   └── advanced_queries/
│       ├── app/
│       │   ├── main.py
│       │   ├── models.py
│       │   ├── crud.py
│       │   └── schemas.py
│       ├── alembic/
│       ├── seed.py
│       └── README.md       # Complete query guide
├── day31/              # Database Transactions
│   └── transactions_demo/
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── crud.py
│       ├── main.py
│       ├── seed.py
│       └── test_transaction.py
├── day36-38/           # E-Commerce API Project
│   ├── __init__.py
│   └── ecommerce_api/
│       ├── app/
│       │   ├── __init__.py
│       │   ├── api/
│       │   ├── core/
│       │   ├── database/
│       │   ├── models/
│       │   ├── repositories/
│       │   ├── schemas/
│       │   ├── services/
│       │   └── main.py
│       ├── alembic/
│       ├── create_admin.py
│       └── README.md
├── day39-42/
├── day43/              # Modular Architecture Refactor
│   └── modular_structure/
│       └── app/
│           ├── modules/
│           │   ├── users/
│           │   ├── products/
│           │   └── orders/
│           ├── shared/
│           └── main.py
├── day44/              # Configuration Management
│   └── config_management/
│       ├── app/
│       │   └── config.py
│       ├── .env.example
│       └── requirements.txt
├── day45/              # Password Hashing & Authentication
│   └── secure_auth/
│       └── app/
│           ├── shared/
│           │   └── security.py
│           └── modules/
│               └── users/
│                   └── router.py
├── day46-47/           # JWT Authentication
│   └── jwt_auth/
│       └── app/
│           ├── shared/
│           │   ├── security.py
│           │   ├── exception.py
│           │   └── utils.py
│           ├── modules/
│           │   └── users/
│           │       ├── models.py
│           │       ├── schemas.py
│           │       ├── repository.py
│           │       ├── service.py
│           │       └── router.py
│           ├── config.py
│           ├── database.py
│           ├── dependencies.py
│           └── main.py
├── day48/              # OAuth2 Password Flow (NEW)
│   └── oauth2_flow/
│       └── app/
│           ├── shared/
│           │   ├── security.py
│           │   ├── exception.py
│           │   └── utils.py
│           ├── modules/
│           │   └── users/
│           │       ├── models.py
│           │       ├── schemas.py
│           │       ├── repository.py
│           │       ├── service.py
│           │       └── router.py
│           ├── config.py
│           ├── database.py
│           ├── dependencies.py
│           └── main.py
day49/rbac/  (Day 49 RBAC)
├── alembic/
│   └── versions/
│       ├── xxxx_initial_migration.py
│       └── xxxx_add_role_field.py
├── app/
│   ├── modules/
│   │   └── users/
│   │       ├── models.py
│   │       ├── schemas.py
│   │       ├── router.py
│   │       ├── repository.py
│   │       └── service.py
│   ├── dependencies.py
├── day50/             # Refresh Tokens
└── day51-52/          # Permission System
├── day53-56/           # Modular E-Commerce Application
│   └── modular_ecommerce/
│       ├── app/
│       │   ├── main.py
│       │   ├── config.py
│       │   ├── database.py
│       │   ├── modules/
│       │   │   ├── auth/
│       │   │   ├── users/
│       │   │   ├── products/
│       │   │   ├── orders/
│       │   │   └── admin/
│       │   └── shared/
│       ├── alembic/
│       ├── .env.example
│       └── README.md
├── day57/              # Event-Driven Architecture Planning
│       └── event_design.md
├── day58/              # Redis Basics
│   └── redis_basics/
│       ├── docker-compose.yml
│       ├── redis_client.py
│       ├── publisher.py
│       ├── subscriber.py
│       ├── queue_producer.py
│       ├── queue_worker.py
│       └── README.md
├── day59/              # Task Queue System
│   └── task_queue/
│       ├── producer.py        # FastAPI producer
│       ├── consumer.py        # Worker consumer
│       ├── tasks.py           # Task definitions
│       ├── redis_client.py    # Redis helper
│       └── README.md├── day60/              # Event Publisher (Redis Pub/Sub)
│   └── event_publisher/
│       ├── redis_client.py
│       ├── events/
│       │   ├── schemas.py
│       │   └── publisher.py
│       └── main.py
├── day61/              # Event Subscribers & Handlers
│   └── event_subscriber/
│       ├── events/
│       │   ├── handlers.py
│       │   ├── subscriber.py
│       │   └── subscriber_main.py
│       └── main.py
├── day64/              # LLM API Setup
├── day65/              # Gemini API Integration
│   └── gemini_integration/
│       ├── main.py
│       ├── services/
│       │   └── gemini_service.py
│       ├── .env
│       └── requirements.txt
├── day66/              # Multi-Turn Chat with History
│   └── chat_history/
│       ├── main.py
│       ├── services/
│       │   └── gemini_service.py
│       └── requirements.txt
├── day67/              # Streaming Responses (SSE)
│   └── streaming_chat/
│       ├── main.py
│       ├── services/
│       │   └── gemini_service.py
│       └── requirements.txt
├── day69-70/           # AI Chatbot with Database
│   └── chatbot_api/
│       ├── main.py
│       ├── config.py
│       ├── database.py
│       ├── models/
│       │   ├── conversation.py
│       │   └── message.py
│       ├── schemas/
│       ├── crud/
│       ├── services/
│       │   └── gemini_service.py
│       └── routers/
│           └── chat.py
├── day71-72/           # AI-Powered Features with Caching
│   └── chatbot_api/
│       ├── main.py
│       ├── config.py
│       ├── database.py
│       ├── models/
│       ├── schemas/
│       ├── crud/
│       ├── services/
│       │   ├── gemini_service.py
│       │   └── ai_utils.py
│       ├── routers/
│       │   ├── chat.py
│       │   └── ai_features.py
│       └── docker-compose.yml
├── day73-74/           # Security Hardening & Optimization
│   └── chatbot_api/
│       ├── main.py
│       ├── config.py
│       ├── database.py
│       ├── models/
│       ├── schemas/
│       ├── crud/
│       ├── services/
│       │   ├── gemini_service.py
│       │   └── ai_utils.py
│       ├── security/
│       │   └── prompt_safety.py
│       ├── prompts/
│       │   └── utils/
│       │       └── prompt_optimizer.py
│       ├── middleware/
│       │   └── error_handler.py
│       ├── docs/
│       │   └── ai-guide.md
│       ├── routers/
│       │   ├── chat.py
│       │   └── ai_features.py
│       ├── DAY_73-74_GUIDE.md
│       ├── START_HERE.md
│       └── docker-compose.yml
└── requirements.txt
```

## What's Next

This repo is my public accountability. Week 10-11 complete. Moving forward!

The roadmap ahead: CI/CD pipelines, cloud deployment (AWS/GCP), Redis caching, and building a complete production-ready application.

---
