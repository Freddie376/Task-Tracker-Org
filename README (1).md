# Task Tracker CLI

A simple command line app, written in Python, to track what you need to do, what you are working on, and what is done. Tasks are saved in a `tasks.json` file in the folder where you run it.

Project from roadmap.sh: https://roadmap.sh/projects/task-tracker

## Features

- Add, update and delete tasks
- Mark a task as in progress or done
- List all tasks
- List tasks by status: to do, in progress, done, or not done
- Saves tasks in a JSON file, which is created automatically if it does not exist
- Shows clear error messages for wrong input
- Uses only Python's built-in modules (no external libraries)

## Requirements

- Python 3.9 or newer

Check your version with:
```bash
Python 3.11.9
```
## How to run

1. Clone the repository:
   ```bash
   git clone https://github.com/Freddie376/task-tracker.git
   cd task-tracker
   ```
2. Run the script with a command:
   ```bash
   python task_tracker.py add "Buy groceries"
   ```

## Commands

| What you want to do | Command |
|---------------------|---------|
| Add a task | `python task_tracker.py add "Buy groceries"` |
| Update a task | `python task_tracker.py update 1 "Buy groceries and cook dinner"` |
| Delete a task | `python task_tracker.py delete 1` |
| Mark a task as in progress | `python task_tracker.py mark-in-progress 1` |
| Mark a task as done | `python task_tracker.py mark-done 1` |
| List all tasks | `python task_tracker.py list` |
| List tasks to do | `python task_tracker.py list todo` |
| List tasks in progress | `python task_tracker.py list in-progress` |
| List tasks that are done | `python task_tracker.py list done` |
| List tasks that are not done | `python task_tracker.py list not-done` |
| Show the help message | `python task_tracker.py` |

The number after a command (like `1`) is the task ID.

## Example

```bash
$ python task_tracker.py add "Buy groceries"
Task added successfully (ID: 1)

$ python task_tracker.py mark-in-progress 1
Task with ID 1 marked as in-progress.

$ python task_tracker.py list
[1] Buy groceries
    Status:  in-progress
    Created: 2026-10-17 09:15:31
    Updated: 2026-10-17 09:20:05
```

## Task format

Each task is stored in `tasks.json` like this:

```json
{
    "id": 1,
    "description": "Buy groceries",
    "status": "todo",
    "createdAt": "2026-10-17 09:15:31",
    "updatedAt": "2026-10-17 09:15:31"
}
```

| Field | Meaning |
|-------|---------|
| `id` | Unique number for the task |
| `description` | What the task is |
| `status` | `todo`, `in-progress` or `done` |
| `createdAt` | When the task was created |
| `updatedAt` | When the task was last changed |

## Error handling

The app shows a clear message instead of crashing when:
- A task ID does not exist
- A task ID is not a number
- A description or ID is missing
- The list filter is not valid
- `tasks.json` is damaged

## Project structure

```
task-tracker/
├── task_tracker.py   # the application
├── tasks.json        # created automatically when you add a task
└── README.md
```

## What I learned

Developing this project has helped me to learn how to type python commands, fix errors and also add new features.
