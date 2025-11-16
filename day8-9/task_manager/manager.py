from typing import List
from models import Task

class TaskManager:
    """TaskManager class to manage a list of tasks"""
    def __init__(self):
        self.tasks: List[Task] = []  # List to store all tasks

    def add(self, title: str) -> Task:
        """Add a new task to the manager"""
        task_id = len(self.tasks) + 1  # Assign a simple ID based on list length
        new_task = Task(id=task_id, title=title)  
        self.tasks.append(new_task)  
        return new_task

    def list(self) -> List[Task]:
        """List all tasks"""
        return self.tasks  

    def complete(self, task_id: int) -> bool:
        """Mark a task as completed by its ID"""
        task = self.find_task(task_id) 
        if task:
            task.status = "completed" 
            return True
        return False

    def delete(self, task_id: int) -> bool:
        """Delete a task by its ID"""
        task = self.find_task(task_id)
        if task:
            self.tasks.remove(task) 
            return True
        return False

    def find_task(self, task_id: int) -> Task:
        """Find a task by its ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None  
