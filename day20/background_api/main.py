import asyncio
import time
import logging
from fastapi import FastAPI, BackgroundTasks, Request
from models import UserCreate, UserResponse

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI()
users = []


# Background Task Function
async def send_email_simulation(user_email: str):
    """
    Simulate sending an email asynchronously.

    Args:
        user_email (str): The email address of the user to send email to.

    Logic:
        - Waits for 2 seconds to simulate email sending delay.
        - Logs a message after "sending" the email.
    """
    await asyncio.sleep(2)  
    logging.info(f"Email sent to {user_email}")


# Middleware 1: Request Timer
@app.middleware("http")
async def request_timer(request: Request, call_next):
    """
    Middleware to measure and log the processing time of each HTTP request.

    Args:
        request (Request): The incoming request object.
        call_next (Callable): Function to call the actual endpoint.

    Logic:
        - Records the start time before executing the endpoint.
        - Calls the endpoint using call_next.
        - Calculates the duration after the endpoint finishes.
        - Logs the HTTP method, path, and duration in seconds.
        - Returns the response.
    """
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logging.info(f"{request.method} {request.url.path} completed in {duration:.2f} sec")
    return response

# Middleware 2: Custom Header
@app.middleware("http")
async def add_custom_header(request: Request, call_next):
    """
    Middleware to add a custom header to all HTTP responses.

    Args:
        request (Request): The incoming request object.
        call_next (Callable): Function to call the actual endpoint.

    Logic:
        - Calls the endpoint using call_next.
        - Adds header 'X-Powered-By' with value 'FastAPI' to the response.
        - Returns the response.
    """
    response = await call_next(request)
    response.headers["X-Powered-By"] = "FastAPI"
    return response

# POST /users endpoint
@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, background_tasks: BackgroundTasks):
    """
    Endpoint to create a new user and trigger a background task.

    Args:
        user (UserCreate): Pydantic model containing user details (name, email, age).
        background_tasks (BackgroundTasks): FastAPI object to run background tasks.

    Logic:
        - Generates a new user ID.
        - Creates a UserResponse object and appends it to the users list.
        - Triggers `send_email_simulation` as a background task.
        - Logs the creation of the user.
        - Returns the user data as response.
    """
    user_id = len(users) + 1
    user_data = UserResponse(
        id=user_id,
        name=user.name,
        email=user.email,
        age=user.age
    )
    users.append(user_data)

    # Trigger background task (email simulation)
    background_tasks.add_task(send_email_simulation, user.email)

    logging.info(f"User created: {user_data}")
    return user_data

# GET /users endpoint
@app.get("/users", response_model=list[UserResponse])
async def get_users():
    """
    Endpoint to retrieve all users.

    Logic:
        - Logs the number of users retrieved.
        - Returns the users list as response.
    """
    logging.info(f"Retrieved {len(users)} users")
    return users
