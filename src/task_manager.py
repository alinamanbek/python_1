''' 
import csv
from datetime import datetime
from task import Task, PersonalTask, WorkTask

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.task_list_file_name = "task_list.csv"

    def add_task(self, task):
        self.tasks.append(task) 

    def list_tasks(self, flag=None):
        for task in self.tasks:
            if flag is None or task.flag == flag:
                print(task)

    def delete_task(self, task_id):
        task = None
        for t in self.tasks:
            if t._task_id == task_id:
                task = t
                break  # Found the task, exit the loop

        if task:
           self.tasks.remove(task)
           print(f"Task ID {task_id} has been deleted.")
        else:
           print("Task not found")

   

    def save_tasks(self):
        with open(self.task_list_file_name, "w", newline="") as file:
            writer = csv.writer(file) 
            writer.writerow(["task_id", "title", "due_date", "status", "description", "flag", "priority", "team_members"])
            for task in self.tasks:
                if isinstance(task, PersonalTask):
                    writer.writerow([task._task_id, task.title, task.due_date, task.status, task._description, 
                                     task.flag, task.priority, ""])
                elif isinstance(task, WorkTask):
                    writer.writerow([task._task_id, task.title, task.due_date, task.status, task._description, 
                                     task.flag, "", ",".join(task.team_members)])
        
    def load_tasks(self):
        self.tasks = [] 
        with open(self.task_list_file_name, "r") as file:
            reader = csv.reader(file)
            next(reader)    
            for row in reader:
                task_id, title, due_date, status, description, flag, priority, team_members = row
                if flag == "personal":
                    task = PersonalTask(title, due_date, description, priority)
                elif flag == "work":
                    task = WorkTask(title, due_date, description)
                    task.team_members = team_members.split(",") if team_members else []
                task._task_id = int(task_id)
                task.status = status
                self.tasks.append(task)
        print("Tasks loaded from file.")

    def get_pending_tasks(self):
        pending_tasks = filter(lambda t: t.status == "pending", self.tasks)
        for task in pending_tasks:
            print(task)

    def get_overdue_tasks(self):
        today = datetime.now().date()
        overdue_tasks = [task for task in self.tasks if task.status == "pending" and datetime.strptime(task.due_date, "%Y-%m-%d").date() < today]
        for task in overdue_tasks:


'''
import sqlite3
from task import Task

class TaskManager:
    def __init__(self):
        self.initialize_db()  # Ensure DB is created on initialization

    def initialize_db(self):
        """Creates the database and table if they don't exist."""
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due_date TEXT NOT NULL,
            description TEXT,
            priority TEXT NOT NULL,
            task_type TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
        ''')
        connection.commit()
        connection.close()

    def add_task(self, task):
        task.save_to_db()

    def list_tasks(self, task_type=None):
        tasks = Task.get_all_tasks(task_type)
        for task in tasks:
            print(task.__dict__)

    def delete_task(self, task_id):
        task = Task.get_task_by_id(task_id)
        if task:
            task.delete_from_db()

    def load_tasks(self):
        tasks = Task.get_all_tasks()
        return tasks
