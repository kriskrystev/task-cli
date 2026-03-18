# Task CLI

A simple command-line interface (CLI) application for managing tasks, built with Python and Typer.

## Features

- ✅ Create new tasks
- 📋 List all tasks
- 🔍 Get specific task details
- ✏️ Update existing tasks
- 🗑️ Delete tasks

## Project Structure
```
TaskCLI/ 
├── pyproject.toml 
├── src/ 
│ └── tasks/ 
│ ├── __init__.py 
│ ├── __main__.py 
│ ├── cli.py
│ └── task.py 
└── README
```

### Prerequisites

- Python 3.7 or higher
- pipx (recommended for installation) or pip

### Install from source

#### Using pipx (Recommended)

1. Install pipx if you haven't already:
   ```bash
   # On Windows
   py -m pip install --user pipx
   py -m pipx ensurepath

   # On macOS/Linux
   python3 -m pip install --user pipx
   python3 -m pipx ensurepath
   ```

2. Clone the repository:
   ```bash
   git clone <repository-url>
   cd task-cli
   ```

3. Install the package:
   ```bash
   # On Windows
   py -m pipx install --force .

   # On macOS/Linux
   pipx install --force .
   ```

## Usage

After installation, you can use the `task-cli` command to manage your tasks:

### Create a task

```bash
# Create a task with just a title
task-cli create-task "Buy groceries"

# Create a task with title and description
task-cli create-task "Buy groceries" --description "Milk, eggs, bread, and vegetables"

# Create a task with title, description, and status
task-cli create-task "Buy groceries" --description "Milk, eggs, bread, and vegetables" --status "in-progress"

# Create a task with all parameters
task-cli create-task "Finish project documentation" --description "Complete API docs and user guide" --status "todo"
```
### List all tasks

```bash
# Show all tasks
task-cli list-tasks
```
### Get task details

```bash
# Get details of a specific task by ID
task-cli get-task f78da9fc-66b8-40ef-ad46-a642e0aa9034
```


### Update a task

```bash
# Update task title
task-cli update-task f78da9fc-66b8-40ef-ad46-a642e0aa9034 --name "Updated task title"

# Update task description
task-cli update-task f78da9fc-66b8-40ef-ad46-a642e0aa9034 --description "Updated description"

# Update task status
task-cli update-task f78da9fc-66b8-40ef-ad46-a642e0aa9034 --status "completed"

# Update multiple fields at once
task-cli update-task f78da9fc-66b8-40ef-ad46-a642e0aa9034 --name "New title" --description "New description" --status "in-progress"
```


### Delete a task

```bash
# Delete a task by ID
task-cli delete-task f78da9fc-66b8-40ef-ad46-a642e0aa9034
```

