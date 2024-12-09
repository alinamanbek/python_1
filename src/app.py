import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Database setup - Create table if it doesn't exist
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT NOT NULL,
            priority TEXT,
            task_type TEXT,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

# Call init_db to ensure the table is created when the app starts
init_db()

# Function to get the database connection
def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

# Create Task Endpoint
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    priority = data.get('priority')
    task_type = data.get('type')

    if not title or not due_date:
        return jsonify({'message': 'Title and due_date are required!'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, due_date, priority, task_type)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, description, due_date, priority, task_type))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return jsonify({'message': 'Task created successfully', 'id': task_id}), 201

# Get All Tasks or Filter by Task Type
@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_type = request.args.get('type')
    conn = get_db_connection()
    cursor = conn.cursor()

    if task_type:
        cursor.execute('SELECT * FROM tasks WHERE task_type = ?', (task_type,))
    else:
        cursor.execute('SELECT * FROM tasks')

    tasks = cursor.fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

# Get Task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    conn.close()

    if task:
        return jsonify(dict(task))
    else:
        return jsonify({'message': 'Task not found'}), 404

# Update Task by ID
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Dynamically update only provided fields
    fields = []
    values = []
    for key in ['title', 'description', 'due_date', 'priority', 'task_type', 'status']:
        if key in data:
            fields.append(f"{key} = ?")
            values.append(data[key])
    if not fields:
        return jsonify({'message': 'No fields to update'}), 400

    values.append(task_id)
    cursor.execute(f'UPDATE tasks SET {", ".join(fields)} WHERE id = ?', values)
    conn.commit()
    conn.close()

    return jsonify({'message': 'Task updated successfully'})

# Delete Task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Task deleted successfully'})

# Get Pending Tasks
@app.route('/tasks/pending', methods=['GET'])
def get_pending_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE status = "pending"')
    tasks = cursor.fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

# Get Overdue Tasks
@app.route('/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    today = datetime.now().strftime('%Y-%m-%d')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE due_date < ? AND status = "pending"', (today,))
    tasks = cursor.fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

if __name__ == '__main__':
    app.run(debug=True)
