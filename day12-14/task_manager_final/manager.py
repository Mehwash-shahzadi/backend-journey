from typing import List, Optional
from datetime import datetime, timedelta
import csv

from models import Task, Priority


class TaskManager:
    """Manage tasks and provide persistence-friendly operations."""

    def __init__(self, sorter=None):
        """
        Initialize TaskManager.

        sorter: optional strategy object with method sort(tasks)
        """
        self.tasks: List[Task] = []
        self.sorter = sorter


    # Core operations 
    def add(self, title: str, priority: Priority = Priority.MEDIUM, tags: Optional[List[str]] = None) -> Task:
        """Add a new task (Day 12)."""
        task_id = len(self.tasks) + 1
        tags = tags or []
        task = Task(id=task_id, title=title, priority=priority, tags=tags)
        self.tasks.append(task)
        return task

    def complete(self, task_id: int) -> bool:
        """Mark task completed by id."""
        task = self.find_task(task_id)
        if task:
            task.status = "completed"
            return True
        return False

    def delete(self, task_id: int) -> bool:
        """Delete a task by id."""
        task = self.find_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def find_task(self, task_id: int) -> Optional[Task]:
        """Return Task object by id or None."""
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None


    # Listing & filtering 
    def list(self,
             status: Optional[str] = None,
             priority: Optional[Priority] = None,
             tag: Optional[str] = None,
             sort_desc: bool = False) -> List[Task]:
        tasks = list(self.tasks)  # copy

        # Filter by status
        if status:
            tasks = [t for t in tasks if t.status == status]

        # Filter by priority
        if priority:
            tasks = [t for t in tasks if t.priority == priority]

        # Filter by tag
        if tag:
            tasks = [t for t in tasks if tag in t.tags]

        # Apply strategy sorter if provided
        if self.sorter:
            tasks = self.sorter.sort(tasks)
        else:
            # default sort by created_at
            tasks.sort(key=lambda t: t.created_at)

        if sort_desc:
            tasks.reverse()

        return tasks

    # export to CSV
    def export_to_csv(self, filename: str = "tasks_export.csv") -> None:
        """
        Export current tasks to CSV.
        Columns: id,title,status,created_at,priority,tags
        """
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["id", "title", "status", "created_at", "priority", "tags"])
            for t in self.tasks:
                writer.writerow([
                    t.id,
                    t.title,
                    t.status,
                    t.created_at.isoformat(),
                    t.priority.value,
                    ";".join(t.tags)
                ])

    #statistics
    def statistics(self, overdue_days: int = 7) -> dict:
        """
        Return stats: total, completed_count, completed_pct, overdue_count.

        Overdue rule: a pending task older than `overdue_days` is considered overdue.
        """
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.status == "completed")
        completed_pct = (completed / total * 100) if total else 0.0

        cutoff = datetime.now() - timedelta(days=overdue_days)
        overdue = sum(1 for t in self.tasks if t.status == "pending" and t.created_at < cutoff)

        return {
            "total": total,
            "completed": completed,
            "completed_pct": round(completed_pct, 2),
            "overdue": overdue
        }

    #iterable support
    def __len__(self) -> int:
        """Return number of tasks (Day 10)."""
        return len(self.tasks)

    def __getitem__(self, index: int) -> Task:
        """Allow indexing & iteration (Day 10)."""
        return self.tasks[index]
