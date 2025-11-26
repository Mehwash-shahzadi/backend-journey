from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")
