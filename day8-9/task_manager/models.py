from datetime import datetime
from dataclasses import dataclass

@dataclass
class Task:
    """Task class to represent a single task"""
    id: int  
    title: str  
    status: str = "pending"  
    created_at: datetime = datetime.now()  

    def __str__(self):
        return f"[{self.status.upper()}] {self.title} (Created: {self.created_at})"

    def to_dict(self):
        """Convert the Task object to a dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at.isoformat()  # Serialize datetime as string
        }

    @staticmethod
    def from_dict(data):
        """Create a Task object from a dictionary (deserialization)"""
        return Task(
            id=data["id"],
            title=data["title"],
            status=data["status"],
            created_at=datetime.fromisoformat(data["created_at"])
        )
