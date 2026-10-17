"""Task Tracker CLI Application
This application allows users to manage their tasks through a command-line interface.
Tasks are saved in a tasks.json file in the current working directory."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from typing import Any, cast

TASK_FILE: str = "tasks.json"
LIST_FILTERS: tuple[str, ...] = ("todo", "in-progress", "done", "not-done")


def current_time() -> str:
    """Returns the current time as a string in the format YYYY-MM-DD HH:MM:SS."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_tasks() -> list[Any]:
    """Loads tasks from the tasks.json file. If the file does not exist, returns an empty list."""
    if not os.path.exists(TASK_FILE):
        return []

    try:
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.strip():
            return []

        tasks = json.loads(content)
        if not isinstance(tasks, list):
            raise ValueError("tasks.json does not contain a list of tasks")
        return cast(list[Any], tasks)
    except (json.JSONDecodeError, ValueError):
        print("Error: tasks.json is not valid. Fix or delete the file and try again.")
        sys.exit(1)


def save_tasks(tasks: list[Any]) -> None:
    """Saves tasks to the tasks.json file."""
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)


def get_next_id(tasks: list[Any]) -> int:
    """Returns the next task ID based on the existing tasks."""
    return max((task["id"] for task in tasks), default=0) + 1


def parse_task_id(value: str) -> int:
    """Converts the typed ID to a number. Stops with a clear message if it is not a number."""
    try:
        return int(value)
    except ValueError:
        print(f"Error: '{value}' is not a valid task ID. Use a number, for example: 1")
        sys.exit(1)


def find_task_by_id(tasks: list[dict[str, Any]], task_id: int) -> dict[str, Any] | None:
    """Finds a task by its ID."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def add_task(description: str) -> None:
    """Adds a new task to the task list."""
    tasks = load_tasks()
    new_id = get_next_id(tasks)
    now = current_time()
    tasks.append(
        {
            "id": new_id,
            "description": description,
            "status": "todo",
            "createdAt": now,
            "updatedAt": now,
        }
    )
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")


def update_task(task_id: int, description: str) -> None:
    """Updates the description of an existing task."""
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)
    if task is None:
        print(f"Task with ID {task_id} not found.")
        return

    task["description"] = description
    task["updatedAt"] = current_time()
    save_tasks(tasks)
    print(f"Task with ID {task_id} updated successfully.")


def delete_task(task_id: int) -> None:
    """Deletes a task by its ID."""
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)
    if task is None:
        print(f"Task with ID {task_id} not found.")
        return

    tasks.remove(task)
    save_tasks(tasks)
    print(f"Task with ID {task_id} deleted successfully.")


def mark_task(task_id: int, status: str) -> None:
    """Marks a task as 'in-progress' or 'done'."""
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)
    if task is None:
        print(f"Task with ID {task_id} not found.")
        return

    task["status"] = status
    task["updatedAt"] = current_time()
    save_tasks(tasks)
    print(f"Task with ID {task_id} marked as {status}.")


def list_tasks(status: str | None = None) -> None:
    """Lists all tasks, optionally filtered by status."""
    tasks = load_tasks()
    if status == "not-done":
        tasks = [task for task in tasks if task["status"] != "done"]
    elif status is not None:
        tasks = [task for task in tasks if task["status"] == status]

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(f"[{task['id']}] {task['description']}")
        print(f"    Status:  {task['status']}")
        print(f"    Created: {task['createdAt']}")
        print(f"    Updated: {task['updatedAt']}")


def show_help() -> None:
    """Displays the help message."""
    print("Task Tracker CLI Application")
    print("Usage:")
    print('  python task_tracker.py add "Buy groceries"')
    print('  python task_tracker.py update 1 "Buy groceries and cook dinner"')
    print("  python task_tracker.py delete 1")
    print("  python task_tracker.py mark-in-progress 1")
    print("  python task_tracker.py mark-done 1")
    print("  python task_tracker.py list")
    print("  python task_tracker.py list todo")
    print("  python task_tracker.py list in-progress")
    print("  python task_tracker.py list done")
    print("  python task_tracker.py list not-done")


def main() -> None:
    """Main function to handle command-line arguments and execute corresponding functions."""
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "add":
        description = " ".join(sys.argv[2:]).strip()
        if not description:
            print('Error: Task description is required. Example: add "Buy milk"')
            return
        add_task(description)

    elif command == "update":
        if len(sys.argv) < 4:
            print('Error: Task ID and new description are required. Example: update 1 "New text"')
            return
        description = " ".join(sys.argv[3:]).strip()
        update_task(parse_task_id(sys.argv[2]), description)

    elif command == "delete":
        if len(sys.argv) != 3:
            print("Error: Task ID is required for 'delete' command. Example: delete 1")
            return
        delete_task(parse_task_id(sys.argv[2]))

    elif command in ("mark-in-progress", "mark-done"):
        if len(sys.argv) != 3:
            print(f"Error: Task ID is required for '{command}' command. Example: {command} 1")
            return
        status = command.replace("mark-", "")
        mark_task(parse_task_id(sys.argv[2]), status)

    elif command == "list":
        status_filter = None
        if len(sys.argv) > 2:
            status_filter = sys.argv[2].lower()
            if status_filter not in LIST_FILTERS:
                print(f"Error: Invalid status filter '{status_filter}'.")
                print("Use one of: todo, in-progress, done, not-done")
                return
        list_tasks(status_filter)

    else:
        print(f"Error: Unknown command '{command}'.")
        show_help()


if __name__ == "__main__":
    main()
