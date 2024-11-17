
# Task Management System

## Overview
A simple Task Management System in Python that allows users to manage tasks (personal or work), view pending/overdue tasks, and save/load tasks from a CSV file.

## Features
- Create personal/work tasks
- View tasks by type
- Delete tasks by ID
- Save/load tasks from CSV
- View pending and overdue tasks

## Setup Instructions

### Requirements
- Python 3.x

### Running the Program
1. Clone or download the project.
2. Navigate to the project directory.
3. Run the following:
   ```bash
   python main.py
   ```

## Classes & Methods

1. **Task Class**
   - Manages task details (ID, title, due date, description, status).
   - `mark_completed()`: Marks task as completed.
   - `str()`: Returns task info as a string.
   - `description.setter`: Validates description (max 15 characters).

2. **PersonalTask Class** (inherits Task)
   - Adds priority handling (`low`, `medium`, `high`).
   - `is_high_priority()`: Checks if task priority is high.
   - `set_priority()`: Sets task priority.

3. **WorkTask Class** (inherits Task)
   - Manages team members.
   - `add_team_member()`: Adds team members.

4. **TaskManager Class**
   - Manages tasks (add, list, delete, save/load).
   - `add_task()`: Adds a task.
   - `list_tasks()`: Lists tasks by type.
   - `delete_task()`: Deletes task by ID.
   - `save_tasks()`: Saves tasks to CSV.
   - `load_tasks()`: Loads tasks from CSV.

## Error Handling
- **Description Length**: Raises `ValueError` if description exceeds 15 characters.
- **Invalid Task Type**: Error message for invalid task type input.
- **Invalid Priority**: Error message for invalid priority input.
- **Task Not Found**: Error if task ID is not found when deleting.
 