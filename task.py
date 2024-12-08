import os
import json
from datetime import datetime

class Task:
    def __init__(self, description, priority='medium', due_date=None, completed=False):
        """
        Initialize a task with various attributes.
        
        :param description: Brief description of the task
        :param priority: Task priority (low/medium/high)
        :param due_date: Optional due date for the task
        :param completed: Task completion status
        """
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed
        self.created_at = datetime.now()

    def to_dict(self):
        """Convert task to a dictionary for JSON serialization."""
        return {
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        """Create a task from a dictionary."""
        task = cls(
            description=data['description'],
            priority=data['priority'],
            due_date=data['due_date'],
            completed=data['completed']
        )
        task.created_at = datetime.fromisoformat(data['created_at'])
        return task

class TodoList:
    def __init__(self, filename='tasks.json'):
        """
        Initialize the todo list with a file for persistent storage.
        
        :param filename: JSON file to store tasks
        """
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def add_task(self, description, priority='medium', due_date=None):
        """
        Add a new task to the list.
        
        :param description: Task description
        :param priority: Task priority
        :param due_date: Optional due date
        """
        task = Task(description, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task added: {description}")

    def list_tasks(self, filter_type=None):
        """
        List tasks with optional filtering.
        
        :param filter_type: Filter by 'completed' or 'pending'
        """
        if not self.tasks:
            print("No tasks found.")
            return

        filtered_tasks = self.tasks
        if filter_type == 'completed':
            filtered_tasks = [task for task in self.tasks if task.completed]
        elif filter_type == 'pending':
            filtered_tasks = [task for task in self.tasks if not task.completed]

        for idx, task in enumerate(filtered_tasks, 1):
            status = "✓" if task.completed else " "
            print(f"{idx}. [{status}] {task.description} (Priority: {task.priority})")

    def mark_task_complete(self, task_index):
        """
        Mark a task as complete.
        
        :param task_index: Index of task to mark complete
        """
        try:
            task = self.tasks[task_index - 1]
            task.completed = True
            self.save_tasks()
            print(f"Task marked complete: {task.description}")
        except IndexError:
            print("Invalid task index.")

    def remove_task(self, task_index):
        """
        Remove a task from the list.
        
        :param task_index: Index of task to remove
        """
        try:
            removed_task = self.tasks.pop(task_index - 1)
            self.save_tasks()
            print(f"Task removed: {removed_task.description}")
        except IndexError:
            print("Invalid task index.")

    def save_tasks(self):
        """Save tasks to a JSON file."""
        with open(self.filename, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=2)

    def load_tasks(self):
        """Load tasks from a JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    task_data = json.load(f)
                    self.tasks = [Task.from_dict(task) for task in task_data]
            except (json.JSONDecodeError, FileNotFoundError):
                self.tasks = []

def main_menu():
    """Display the main menu and handle user interactions."""
    todo_list = TodoList()

    while True:
        print("\n--- Todo List Application ---")
        print("1. Add Task")
        print("2. List All Tasks")
        print("3. List Pending Tasks")
        print("4. List Completed Tasks")
        print("5. Mark Task as Complete")
        print("6. Remove Task")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            description = input("Enter task description: ")
            priority = input("Enter priority (low/medium/high, default medium): ") or 'medium'
            todo_list.add_task(description, priority)
        elif choice == '2':
            todo_list.list_tasks()
        elif choice == '3':
            todo_list.list_tasks('pending')
        elif choice == '4':
            todo_list.list_tasks('completed')
        elif choice == '5':
            todo_list.list_tasks()
            task_index = int(input("Enter task number to mark complete: "))
            todo_list.mark_task_complete(task_index)
        elif choice == '6':
            todo_list.list_tasks()
            task_index = int(input("Enter task number to remove: "))
            todo_list.remove_task(task_index)
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()