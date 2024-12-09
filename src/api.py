from task_1 import Task, PersonalTask, WorkTask  # Only this import is needed
from task_manager import TaskManager

def main():
    manager = TaskManager()

    # Ensure the table is created at the beginning
    task = Task("Test Task", "2024-12-31")  # Create a temporary task
    task.save_to_db()  # This will create the table if it doesn't exist

    manager.load_tasks()  # Ensure the tasks are loaded from DB at start

    while True:
        print("\nTask Management System")
        print("1. Create a Task")
        print("2. View All Tasks")
        print("3. Delete a Task")
        print("4. Save Tasks")
        print("5. Load Tasks")
        print("6. View Pending Tasks")
        print("7. View Overdue Tasks")
        print("8. Exit")
        choice = input("Enter your choice(only numbers): ")

        if choice == "1":
            task_type = input("Enter task type (personal/work): ").lower()
            title = input("Title: ")
            due_date = input("Due date (YYYY-MM-DD): ")
            description = input("Description (15 chars max): ")

            task = None
            if task_type == "personal":
                priority = input("Priority (low, medium, high): ")
                task = PersonalTask(title, due_date, description, priority)
            elif task_type == "work":
                task = WorkTask(title, due_date, description)
                members = input("Enter team members (comma-separated): ").split(',')
                for member in members:
                    task.add_team_member(member.strip())
            else:
                print("Invalid task type. Please enter 'personal' or 'work'.")

            if task is not None:
                manager.add_task(task)
                print("Task added!")

        elif choice == "2":
            flag = input("Filter by task type (personal/work/none): ").lower()
            manager.list_tasks(flag)

        elif choice == "3":
            task_id = int(input("Enter task ID to delete: "))
            manager.delete_task(task_id)

        elif choice == "4":
            manager.save_tasks()
            print("Tasks saved to database.")

        elif choice == "5":
            manager.load_tasks()
            print("Tasks loaded from database.")

        elif choice == "6":
            print("Pending Tasks:")
            manager.get_pending_tasks()

        elif choice == "7":
            print("Overdue Tasks:")
            manager.get_overdue_tasks()
        elif choice == "8":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
