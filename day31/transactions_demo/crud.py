from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
from . import models

def create_user(db: Session, name: str, email: str, balance: float):
    try:
        user = models.User(name=name, email=email, balance=balance)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise ValueError("Email must be unique!")


def transfer_money(db: Session, sender_id: int, receiver_id: int, amount: float):
    try:
        sender = db.query(models.User).filter(models.User.id == sender_id).first()
        receiver = db.query(models.User).filter(models.User.id == receiver_id).first()

        if not sender or not receiver:
            raise ValueError("User not found")

        amount = Decimal(str(amount))

        if sender.balance < amount:
            raise ValueError("Not enough balance")

        # Step 1: deduct
        sender.balance -= amount

        # Step 2: add
        receiver.balance += amount

        db.commit()
        return {"message": "Transfer successful"}

    except Exception as e:
        db.rollback()
        raise