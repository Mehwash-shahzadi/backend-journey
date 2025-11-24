from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine
from dependencies import get_db
import crud

# Create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Create User
@app.post("/users")
def create_user(email: str, name: str, db: Session = Depends(get_db)):
    # Check duplicate email
    existing = db.query(crud.User).filter(crud.User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    return crud.create_user(db, email, name)



# Get all users
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)


# Get one user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# Update user
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# Delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted"}
