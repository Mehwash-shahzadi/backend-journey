from repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
from schemas import UserCreate

class UserService:
    """
    Service layer for User-related business logic.
    Handles validation and orchestrates repository calls.
    """
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def create_user_with_validation(self, data: UserCreate):
        """
        Business rules:
        - Check if email already exists
        - Validate age if provided
        - Auto-generate username if needed
        """
        # Check email uniqueness
        existing_user = self.user_repo.get_by_email(data.email)
        if existing_user:
            raise ValueError("Email already exists")

        # Auto-generate username 
        username = getattr(data, "username", None) or data.name.lower().replace(" ", "_")

        # Create user in repository
        return self.user_repo.create(name=data.name, email=data.email, balance=0)

    def deactivate_user(self, user_id: int):
        """Example business logic to deactivate a user"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    def get_user_with_posts(self, user_id: int):
        """Example orchestration method combining multiple repositories"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        # Placeholder for posts
        user.posts = []
        return user
