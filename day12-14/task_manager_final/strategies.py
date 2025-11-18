from typing import List
from models import Task, Priority


class SortByDate:
    """Sort tasks by creation date (oldest first)."""
    def sort(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: t.created_at)


class SortByPriority:
    """Sort tasks by priority (HIGH -> LOW)."""
    # Map Priority to numeric ordering (higher value = higher importance)
    _rank = {Priority.HIGH: 3, Priority.MEDIUM: 2, Priority.LOW: 1}

    def sort(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: self._rank.get(t.priority, 2), reverse=True)
