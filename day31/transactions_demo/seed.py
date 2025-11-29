from .database import SessionLocal, engine
from .models import Base
from . import models

Base.metadata.create_all(bind=engine)

db = SessionLocal()

if not db.query(models.User).filter_by(email="asif@mail.com").first():
    user1 = models.User(name="Asif", email="asif@mail.com", balance=100)
    db.add(user1)

if not db.query(models.User).filter_by(email="ali@mail.com").first():
    user2 = models.User(name="Ali", email="ali@mail.com", balance=50)
    db.add(user2)

db.commit()
db.close()

print("Seed data added!")