from typing import List
from models import Task


class TaskManager:
    def __init__(self, sorter=None):
        '''Initialize TaskManager with an optional sorting strategy'''
        self.tasks: List[Task] = []
        self.sorter = sorter  # Strategy pattern: sorter can be any sorting strategy

    def add(self, title: str, priority: int = 1) -> Task:
        '''Add a new task with a title and priority'''
        task_id = len(self.tasks) + 1
        new_task = Task(id=task_id, title=title, priority=priority)
        self.tasks.append(new_task)
        return new_task

    def list(self):
        """Return tasks using the active strategy (if any)"""
        if self.sorter:
            return self.sorter.sort(self.tasks)
        return self.tasks

    def complete(self, task_id: int) -> bool:
        '''Mark a task as completed by its ID'''
        task = self.find_task(task_id)
        if task:
            task.status = "completed"
            return True
        return False

    def delete(self, task_id: int) -> bool:
        '''Delete a task by its ID'''
        task = self.find_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def find_task(self, task_id: int):
        '''Find a task by its ID'''
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    #magic methods 
    def __len__(self):
        """Allows len(manager)"""
        return len(self.tasks)

    def __getitem__(self, index):
        """Allows indexing & iteration"""
        return self.tasks[index]
