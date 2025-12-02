from repositories.base_repository import BaseRepository
from models import User

class UserRepository(BaseRepository):

    def get_all(self):
        return self.db.query(User).all()

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create(self, name: str, email: str, balance: float):
        user = User(name=name, email=email, balance=balance)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
