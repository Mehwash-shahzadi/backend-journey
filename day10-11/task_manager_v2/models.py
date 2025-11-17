from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    id: int
    title: str
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    priority: int = 1   # New field for priority 


    #magic methods
    def __str__(self):
        """Human-readable format"""
        return f"{self.id}. {self.title} ({self.status}, priority={self.priority})"

    def __repr__(self):
        """Debug-friendly format"""
        return (f"Task(id={self.id}, title='{self.title}', "
                f"status='{self.status}', created_at='{self.created_at}', "
                f"priority={self.priority})")

    def __eq__(self, other):
        """Task equality based only on ID"""
        if not isinstance(other, Task):
            return NotImplemented
        return self.id == other.id

    def __lt__(self, other):
        """Default sorting: by created_at"""
        if not isinstance(other, Task):
            return NotImplemented
        return self.created_at < other.created_at

    # Convert task to dict (for JSON)
    def to_dict(self):
        '''Convert Task to dictionary for serialization'''
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "priority": self.priority
        }

    @staticmethod
    def from_dict(data):
        '''Create Task from dictionary (deserialization)'''
        return Task(
            id=data["id"],
            title=data["title"],
            status=data["status"],
            created_at=datetime.fromisoformat(data["created_at"]),
            priority=data.get("priority", 1)
        )
