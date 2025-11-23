import asyncio
import httpx
from fastapi import FastAPI, HTTPException
from models import UserCreate, UserResponse

app = FastAPI()

# In-memory storage
users = []

# Convert CRUD to async

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Create a new user."""
    user_id = len(users) + 1
    user_data = UserResponse(
        id=user_id,
        name=user.name,
        email=user.email,
        age=user.age
    )
    users.append(user_data)
    return user_data


@app.get("/users", response_model=list[UserResponse])
async def get_users():
    """Get all users."""
    return users


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Retrieve a single user by ID ."""
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, updated_user: UserCreate):
    """Update a user ."""
    for index, user in enumerate(users):
        if user.id == user_id:
            user_data = UserResponse(
                id=user_id,
                name=updated_user.name,
                email=updated_user.email,
                age=updated_user.age
            )
            users[index] = user_data
            return user_data
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Delete a user."""
    for index, user in enumerate(users):
        if user.id == user_id:
            del users[index]
            return {"detail": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

# slow async sleep

@app.get("/slow")
async def slow_endpoint():
    """Simulate slow database operation."""
    await asyncio.sleep(2)
    return {"message": "Finished after 2 seconds"}


# external call public API
@app.get("/external")
async def fetch_external_users():
    """
    Fetch users from external API using async httpx.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/users")

    return {
        "status": response.status_code,
        "data": response.json()
    }
