import sqlite3  # Import sqlite3 to avoid NameError
from flask import Flask, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize the app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='pending')

    def __repr__(self):
        return f'<Task {self.title}>'

    # Save task to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Load task from the database by its ID
    @classmethod
    def load_from_db(cls, task_id):
        return cls.query.get(task_id)

    # Update task in the database
    def update_in_db(self):
        db.session.commit()

    # Delete task from the database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

# Initialize the database and create tables if needed
def initialize_db():
    connection = sqlite3.connect('tasks.db')  # sqlite3 needs to be imported
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due_date TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            task_type TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    ''')
    connection.commit()
    connection.close()

# Initialize DB and create all tables
initialize_db()

# Create the database (using Flask-SQLAlchemy)
with app.app_context():
    db.create_all()

# Routes

# Route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'due_date': task.due_date,
        'description': task.description,
        'priority': task.priority,
        'task_type': task.task_type,
        'status': task.status
    } for task in tasks])

# Route to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(
        title=data['title'],
        due_date=data['due_date'],
        description=data['description'],
        priority=data['priority'],
        task_type=data['task_type']
    )
    task.save_to_db()
    return jsonify({'message': 'Task created successfully', 'task': {
        'id': task.id,
        'title': task.title,
        'due_date': task.due_date,
        'description': task.description,
        'priority': task.priority,
        'task_type': task.task_type,
        'status': task.status
    }}), 201

# Route to update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Task.load_from_db(task_id)
    if task:
        task.title = data.get('title', task.title)
        task.due_date = data.get('due_date', task.due_date)
        task.description = data.get('description', task.description)
        task.priority = data.get('priority', task.priority)
        task.task_type = data.get('task_type', task.task_type)
        task.status = data.get('status', task.status)
        task.update_in_db()
        return jsonify({'message': 'Task updated successfully', 'task': {
            'id': task.id,
            'title': task.title,
            'due_date': task.due_date,
            'description': task.description,
            'priority': task.priority,
            'task_type': task.task_type,
            'status': task.status
        }})
    return jsonify({'message': 'Task not found'}), 404

# Route to delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.load_from_db(task_id)
    if task:
        task.delete_from_db()
        return jsonify({'message': 'Task deleted successfully'})
    return jsonify({'message': 'Task not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
