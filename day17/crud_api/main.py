from fastapi import FastAPI, HTTPException
from models import UserCreate, UserResponse

app = FastAPI()

users = []

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
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
def get_users():
    '''Retrieve all users.'''
    return users


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    '''Retrieve a user by ID.'''
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserCreate):
    '''Update a user's information.'''
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
def delete_user(user_id: int):
    '''Delete a user by ID.'''
    for index, user in enumerate(users):
        if user.id == user_id:
            del users[index]
            return {"detail": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")