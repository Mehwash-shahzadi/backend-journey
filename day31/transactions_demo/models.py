from sqlalchemy import Column, Integer, String, Numeric, UniqueConstraint
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    balance = Column(Numeric, default=0)

    __table_args__ = (
        UniqueConstraint("email", name="unique_email_constraint"),
    )
