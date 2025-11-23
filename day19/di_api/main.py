from fastapi import Depends,FastAPI
from dependency import get_pagination,get_user_by_id
from models import UserCreate,UserResponse
app=FastAPI()

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
def get_users(p: dict = Depends(get_pagination)):
    """Retrieve users with pagination."""
    skip = p["skip"]
    limit = p["limit"]
    return users[skip : skip + limit]

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user: UserResponse = Depends(get_user_by_id)):
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(updated_user: UserCreate,existing_user: UserResponse = Depends(get_user_by_id)):
    for index, user in enumerate(users):
        if user.id == existing_user.id:
            new_data = UserResponse(
                id=user.id,
                name=updated_user.name,
                email=updated_user.email,
                age=updated_user.age
            )
            users[index] = new_data
            return new_data
        
@app.delete("/users/{user_id}")
def delete_user(existing_user: UserResponse = Depends(get_user_by_id)):
    for index, user in enumerate(users):
        if user.id == existing_user.id:
            del users[index]
            return {"detail": "User deleted successfully"}
