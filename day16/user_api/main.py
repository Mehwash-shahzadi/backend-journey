from fastapi import FastAPI
from models import UserCreate, UserResponse

app = FastAPI()

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    """Create a new user."""
    # We return only email + age because UserResponse excludes password
    return UserResponse(
        email=user.email,
        age=user.age
    )
