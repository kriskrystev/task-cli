import os
from pathlib import Path

# =========================
# File / environment config
# =========================
TASKS_JSON = "tasks.json"
TASK_CLI_DIR = ".task-cli"
TASK_CLI = "task-cli"
LOCALAPPDATA_ENV = "LOCALAPPDATA"
EMPTY_JSON_LIST = "[]"
UTF8_ENCODING = "utf-8"

# =========================
# Task actions
# =========================
ACTION_CREATE = "create"
ACTION_LIST = "list"
ACTION_DELETE = "delete"
ACTION_UPDATE = "update"

# =========================
# Task field names
# =========================
TASK_FIELD_ID = "id"
TASK_FIELD_NAME = "name"
TASK_FIELD_DESCRIPTION = "description"
TASK_FIELD_STATUS = "status"
TASK_FIELD_CREATED_AT = "created_at"
TASK_FIELD_UPDATED_AT = "updated_at"

# =========================
# CLI help text
# =========================
HELP_NAME = "Name of the task"
HELP_DESCRIPTION = "Description of the task"
HELP_STATUS = "Status of the task"
HELP_TASK_ID = "ID of the task"
HELP_UPDATE_NAME = "New name for the task (optional)"
HELP_UPDATE_DESCRIPTION = "New description for the task (optional)"
HELP_UPDATE_STATUS = "New status for the task (optional)"

# =========================
# Log / user-facing messages
# =========================
LOG_INITIAL_LOAD = "Initial loading tasks from json file"
LOG_BUILDING_TASK = "Building the task"
LOG_APPENDING_TASK = "Appending the task"
LOG_DUMPING_TO_JSON = "Dumping to json file"
LOG_TASK_CREATED = "Task created successfully"
LOG_ATTACHING_CREATED_AT = "Attaching created_at"
LOG_ATTACHING_UPDATED_AT = "Attaching updated_at"
LOG_ATTACHING_ID = "Attaching id"
LOG_LISTING_TASKS = "Listing tasks"
LOG_TASK_DELETED = "Task deleted successfully"
LOG_DELETING_TASK = "Deleting task"
LOG_INVALID_TASK_ID = "Invalid task ID format. Please provide a valid UUID4."
LOG_TASK_NOT_FOUND_TEMPLATE = "Task with ID {task_id} not found"
LOG_UPDATING_TASK = "Updating task"
LOG_TASK_UPDATED = "Task updated successfully"
LOG_NO_FIELDS_TO_UPDATE = "No fields provided to update"
LOG_INVALID_STATUS = "Invalid status. Must be one of: TODO, IN_PROGRESS, IN_REVIEW, DONE"
