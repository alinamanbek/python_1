# Task Management System

## Overview
The **Task Management System** is a Python-based application designed to manage personal and work-related tasks efficiently. Users can create, update, view, and delete tasks, as well as filter tasks by type or status. The application also supports saving and loading tasks from a CSV file.

---

## Features
- **Task Creation**: Add tasks with customizable attributes (title, due date, description, etc.).
- **Task Management**:
  - Update task attributes such as status or priority.
  - View tasks by type (personal or work).
  - Identify pending and overdue tasks.
  - Delete tasks by ID.
- **CSV Integration**: Save tasks to a CSV file and reload them for future use.

---

## Setup Instructions

### Requirements
- **Python**: Version 3.x is required.

### Steps to Run
1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd task-management-system
   ```
2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application**:
   ```bash
   python main.py
   ```

---

## API Documentation

### **Endpoints**

#### 1. Create Task
- **URL**: `/tasks`
- **Method**: `POST`
- **Payload** (JSON):
  ```json
  {
    "title": "Task Title",
    "description": "Optional description",
    "due_date": "YYYY-MM-DD",
    "priority": "low/medium/high",
    "type": "personal/work"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Task created successfully",
    "id": 1
  }
  ```

#### 2. Get All Tasks
- **URL**: `/tasks`
- **Method**: `GET`
- **Query Parameter** (optional): `type` (e.g., `/tasks?type=personal`)
- **Response**:
  ```json
  [
    {
      "id": 1,
      "title": "Task Title",
      "description": "Description",
      "due_date": "YYYY-MM-DD",
      "priority": "low",
      "type": "personal",
      "status": "pending"
    }
  ]
  ```

#### 3. Get Pending Tasks
- **URL**: `/tasks/pending`
- **Method**: `GET`
- **Response**:
  ```json
  [
    {
      "id": 1,
      "title": "Task Title",
      "description": "Description",
      "due_date": "YYYY-MM-DD",
      "priority": "low",
      "type": "personal",
      "status": "pending"
    }
  ]
  ```

#### 4. Get Overdue Tasks
- **URL**: `/tasks/overdue`
- **Method**: `GET`
- **Response**:
  ```json
  [
    {
      "id": 1,
      "title": "Task Title",
      "description": "Description",
      "due_date": "YYYY-MM-DD",
      "priority": "low",
      "type": "personal",
      "status": "pending"
    }
  ]
  ```

#### 5. Update Task
- **URL**: `/tasks/<task_id>`
- **Method**: `PUT`
- **Payload** (JSON):
  ```json
  {
    "description": "Updated description",
    "priority": "high",
    "status": "completed"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Task updated successfully"
  }
  ```

#### 6. Delete Task
- **URL**: `/tasks/<task_id>`
- **Method**: `DELETE`
- **Response**:
  ```json
  {
    "message": "Task deleted successfully"
  }
  ```

---

## Database Schema

- **Table Name**: `tasks`
- **Columns**:
  | Column Name | Type    | Description                               |
  |-------------|---------|-------------------------------------------|
  | `id`        | INTEGER | Auto-incremented primary key             |
  | `title`     | TEXT    | Task title                               |
  | `description`| TEXT   | Optional task description                |
  | `due_date`  | TEXT    | Due date in `YYYY-MM-DD` format          |
  | `priority`  | TEXT    | Task priority (`low/medium/high`)        |
  | `type`      | TEXT    | Task type (`personal/work`)              |
  | `status`    | TEXT    | Task status (`pending/completed`)        |

---

## Example Usage

### **Create a Task**
```bash
curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d '{
  "title": "Finish project",
  "description": "Complete by end of the week",
  "due_date": "2024-12-15",
  "priority": "high",
  "type": "work"
}'
```

### **Get All Tasks**
```bash
curl -X GET http://127.0.0.1:5000/tasks
```

### **Get Pending Tasks**
```bash
curl -X GET http://127.0.0.1:5000/tasks/pending
```

### **Get Overdue Tasks**
```bash
curl -X GET http://127.0.0.1:5000/tasks/overdue
```

### **Update a Task**
```bash
curl -X PUT http://127.0.0.1:5000/tasks/1 -H "Content-Type: application/json" -d '{
  "status": "completed",
  "priority": "medium"
}'
```

### **Delete a Task**
```bash
curl -X DELETE http://127.0.0.1:5000/tasks/1
```

---

## Error Handling

1. **Invalid Input**: Returns `400` with an error message for invalid payloads or missing fields.
2. **Task Not Found**: Returns `404` if the task ID does not exist.
3. **Invalid Query Parameter**: Handles invalid query parameters gracefully.
 