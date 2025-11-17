class SortByDate:
    """Sort tasks by created_at date"""
    def sort(self, tasks):
        return sorted(tasks, key=lambda t: t.created_at)


class SortByPriority:
    """Sort tasks by priority (higher first)"""
    def sort(self, tasks):
        return sorted(tasks, key=lambda t: t.priority, reverse=True)
    
    #“The Strategy Pattern is a design pattern that lets you change an object’s behavior by switching between different algorithms or strategies without modifying the main code.”