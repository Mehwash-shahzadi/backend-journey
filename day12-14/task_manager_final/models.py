from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List


class Priority(Enum):
    """Priority levels for tasks .the values are not normalstrings these are enum objects"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class Task:
    """
    Task dataclass.

    Fields:
    - id: unique integer id
    - title: task title
    - status: 'pending' or 'completed'
    - created_at: timestamp (datetime)
    - priority: Priority enum 
    - tags: list of category strings 
    """
    id: int
    title: str
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    priority: Priority = Priority.MEDIUM
    tags: List[str] = field(default_factory=list)

   
    #magic methods
    def __str__(self) -> str:
        """User-friendly representation."""
        tags = f" tags={self.tags}" if self.tags else ""
        return f"{self.id}. {self.title} [{self.status}] (priority={self.priority.value}){tags}"

    def __repr__(self) -> str:
        """Debug repr."""
        return (f"Task(id={self.id!r}, title={self.title!r}, status={self.status!r}, "
                f"created_at={self.created_at!r}, priority={self.priority!r}, tags={self.tags!r})")

    def __eq__(self, other) -> bool:
        """Equality based on id."""
        if not isinstance(other, Task):
            return NotImplemented
        return self.id == other.id

    def __lt__(self, other) -> bool:
        """Less-than uses created_at by default."""
        if not isinstance(other, Task):
            return NotImplemented
        return self.created_at < other.created_at


    # Serialization helpers (used by storage)
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict ."""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "priority": self.priority.value,
            "tags": self.tags,
        }
    #deserialization 
    @staticmethod
    def from_dict(data: dict) -> "Task":
        """Create Task from dict ."""
        created = datetime.fromisoformat(data["created_at"])
        pr = Priority(data.get("priority", "MEDIUM"))
        tags = data.get("tags", [])
        return Task(
            id=int(data["id"]),
            title=data["title"],
            status=data.get("status", "pending"),
            created_at=created,
            priority=pr,
            tags=tags,
        )
