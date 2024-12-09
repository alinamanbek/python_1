'''
import datetime

class Task:
    _task_counter = 1   

    def __init__(self, title, due_date, description=None, flag="personal"):  
        
        self._task_id = Task._task_counter   
        Task._task_counter += 1
        self.title = title
        self.due_date = due_date
        self.status = "pending"  
        self._description(description)
        self.flag = flag 
        
    def mark_completed(self):
        self.status = "completed"  
    def __str__(self):    
        return f"Task ID: {self._task_id}, Title: {self.title}, Due Date: {self.due_date}, Status: {self.status}"

  
    def get_description(self):   
        return self._description

    def set_description(self, desc):
        if desc is not None and len(desc) > 15: 
            raise ValueError("Description cannot exceed 15 characters")
        self._description = desc  
          
class PersonalTask(Task):
    def __init__(self, title, due_date, description=None, priority="low"):
        super().__init__(title, due_date, description, flag="personal")#--> Calls the parent class atributes
        self.priority = priority

    def is_high_priority(self):  
        return self.priority == "high"

    def set_priority(self, priority):
        if priority in ["high", "medium", "low"]:
            self.priority = priority
        else:
            print("Invalid priority. Use 'high', 'medium', or 'low'.")

    def __str__(self):
        return super().__str__() + f", Priority: {self.priority}"


class WorkTask(Task):
    def __init__(self, title, due_date, description=None):
        super().__init__(title, due_date, description, flag="work")
        self.team_members = []

    def add_team_member(self, member):
        if member:
            self.team_members.append(member)

    def __str__(self):
        return super().__str__() + f", Team Members: {', '.join(self.team_members)}"  #join--> comma-separated string.




'''


 

 

 
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Database initialization function
def initialize_db():
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
        task_type TEXT NOT NULL
    )
    ''')
    connection.commit()
    connection.close()

# Task class to interact with the database
class Task:
    def __init__(self, title, due_date, description, priority, task_type, task_id=None):
        self.task_id = task_id
        self.title = title
        self.due_date = due_date
        self.description = description
        self.priority = priority
        self.task_type = task_type

    def save_to_db(self):
        """Saves the task to the database."""
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, due_date, description, priority, task_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.title, self.due_date, self.description, self.priority, self.task_type))
        connection.commit()
        connection.close()

    @classmethod
    def get_all_tasks(cls):
        """Fetches all tasks from the database."""
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        connection.close()
        return [cls(*row[1:], task_id=row[0]) for row in rows]

    @classmethod
    def get_task_by_id(cls, task_id):
        """Fetches a task by its ID."""
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        connection.close()
        if row:
            return cls(*row[1:], task_id=row[0])
        return None

    @classmethod
    def update_task(cls, task_id, title, due_date, description, priority, task_type):
        """Updates a task's details in the database."""
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE tasks
            SET title = ?, due_date = ?, description = ?, priority = ?, task_type = ?
            WHERE id = ?
        ''', (title, due_date, description, priority, task_type, task_id))
        connection.commit()
        connection.close()

    @classmethod
    def delete_task(cls, task_id):
        """Deletes a task by its ID."""
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        connection.commit()
        connection.close()

# Initialize the database and tables
initialize_db()

# Routes for task management

@app.route('/tasks', methods=['POST'])
def create_task():
    """Creates a new task."""
    data = request.get_json()
    task = Task(
        title=data['title'],
        due_date=data['due_date'],
        description=data.get('description', ''),
        priority=data['priority'],
        task_type=data['type']
    )
    task.save_to_db()
    return jsonify({"message": "Task created successfully!"}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Gets all tasks."""
    tasks = Task.get_all_tasks()
    return jsonify([{
        'id': task.task_id,
        'title': task.title,
        'due_date': task.due_date,
        'description': task.description,
        'priority': task.priority,
        'task_type': task.task_type
    } for task in tasks]), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Gets a specific task by ID."""
    task = Task.get_task_by_id(task_id)
    if task:
        return jsonify({
            'id': task.task_id,
            'title': task.title,
            'due_date': task.due_date,
            'description': task.description,
            'priority': task.priority,
            'task_type': task.task_type
        }), 200
    return jsonify({"message": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Updates a specific task."""
    data = request.get_json()
    Task.update_task(
        task_id,
        title=data['title'],
        due_date=data['due_date'],
        description=data.get('description', ''),
        priority=data['priority'],
        task_type=data['type']
    )
    return jsonify({"message": "Task updated successfully!"}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Deletes a specific task."""
    Task.delete_task(task_id)
    return jsonify({"message": "Task deleted successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
 


