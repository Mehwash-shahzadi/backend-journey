from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import database, models, crud, schemas

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def home():
    return {"message": "Transaction API is running"}

@app.post("/create-user", response_model=schemas.UserSchema)
def create_user(name: str, email: str, balance: float, db: Session = Depends(database.get_db)):
    try:
        return crud.create_user(db, name, email, balance)
    except ValueError as e:
        return {"error": str(e)}


@app.post("/transfer")
def transfer(sender_id: int, receiver_id: int, amount: float, db: Session = Depends(database.get_db)):
    try:
        return crud.transfer_money(db, sender_id, receiver_id, amount)
    except Exception as e:
        db.rollback()
        return {"error": str(e)}