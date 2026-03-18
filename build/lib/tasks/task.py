import datetime as dt
import json
import os
import uuid
from enum import Enum
from pathlib import Path
from typing import Dict

import typer
from typing_extensions import Annotated

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
# Task status enum
# =========================
class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW"
    DONE = "DONE"


DEFAULT_STATUS = TaskStatus.TODO

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


def get_data_file_path() -> Path:
    local_app_data = os.getenv(LOCALAPPDATA_ENV)
    if local_app_data:
        data_dir = Path(local_app_data) / TASK_CLI
    else:
        data_dir = Path.home() / TASK_CLI_DIR

    data_dir.mkdir(parents=True, exist_ok=True)
    data_file = data_dir / TASKS_JSON

    if not data_file.exists():
        data_file.write_text(EMPTY_JSON_LIST, encoding=UTF8_ENCODING)

    return data_file


DATA_TASKS_JSON = get_data_file_path()

with DATA_TASKS_JSON.open("r", encoding=UTF8_ENCODING) as json_data:
    print(LOG_INITIAL_LOAD)
    task_collection = json.load(json_data)


def is_valid_uuid4(uuid_str: str) -> bool:
    try:
        uuid.UUID(uuid_str, version=4)
        return True
    except ValueError:
        return False


def validate_status(status_str: str) -> TaskStatus:
    try:
        return TaskStatus(status_str)
    except ValueError:
        raise ValueError(LOG_INVALID_STATUS)


def create_task(
        name: Annotated[str, typer.Option(help=HELP_NAME)],
        description: Annotated[str, typer.Option(help=HELP_DESCRIPTION)] = None,
        status: Annotated[str, typer.Option(help=HELP_STATUS)] = None,
):
    validated_status = validate_status(status)
    print(LOG_BUILDING_TASK)
    new_task = build_task_dict(name, description, validated_status.value)

    print(LOG_APPENDING_TASK)
    task_collection.append(
        with_updated(
            with_created(
                with_id(new_task)
            )
        )
    )

    with DATA_TASKS_JSON.open("w", encoding=UTF8_ENCODING) as json_file:
        print(LOG_DUMPING_TO_JSON)
        json.dump(task_collection, json_file, indent=4)
        print(LOG_TASK_CREATED)


def list_tasks():
    print(LOG_LISTING_TASKS)
    for task in task_collection:
        print(
            f"Task ID: {task[TASK_FIELD_ID]}, "
            f"Name: {task[TASK_FIELD_NAME]}, "
            f"Status: {task[TASK_FIELD_STATUS]}"
        )

def get_task(task_id: Annotated[str, typer.Argument(help=HELP_TASK_ID)]):
    if not is_valid_uuid4(task_id):
        raise ValueError(LOG_INVALID_TASK_ID)

    for task in task_collection:
        if task[TASK_FIELD_ID] == task_id:
            print(
                f"Task ID: {task[TASK_FIELD_ID]}, "
                f"Name: {task[TASK_FIELD_NAME]}, "
                f"Status: {task[TASK_FIELD_STATUS]}"
            )
    return None


def delete_task(
        task_id: Annotated[str, typer.Argument(help=HELP_TASK_ID)]
):
    if not is_valid_uuid4(task_id):
        raise ValueError(LOG_INVALID_TASK_ID)

    print(LOG_DELETING_TASK)
    task_found = False

    for task in task_collection:
        if task[TASK_FIELD_ID] == task_id:
            task_collection.remove(task)
            with DATA_TASKS_JSON.open("w", encoding=UTF8_ENCODING) as json_file:
                json.dump(task_collection, json_file, indent=4)
            print(LOG_TASK_DELETED)
            task_found = True
            break

    if not task_found:
        print(LOG_TASK_NOT_FOUND_TEMPLATE.format(task_id=task_id))


def update_task(
        task_id: Annotated[str, typer.Option(help=HELP_TASK_ID)],
        name: Annotated[str, typer.Option(help=HELP_UPDATE_NAME)] = None,
        description: Annotated[str, typer.Option(help=HELP_UPDATE_DESCRIPTION)] = None,
        status: Annotated[str, typer.Option(help=HELP_UPDATE_STATUS)] = None,
):
    if not is_valid_uuid4(task_id):
        raise ValueError(LOG_INVALID_TASK_ID)

    if name is None and description is None and status is None:
        print(LOG_NO_FIELDS_TO_UPDATE)
        return

    if status is not None:
        validated_status = validate_status(status)

    print(LOG_UPDATING_TASK)
    task_found = False

    for task in task_collection:
        if task[TASK_FIELD_ID] == task_id:
            if name is not None:
                task[TASK_FIELD_NAME] = name
            if description is not None:
                task[TASK_FIELD_DESCRIPTION] = description
            if status is not None:
                task[TASK_FIELD_STATUS] = validated_status.value

            with_updated(task)

            with DATA_TASKS_JSON.open("w", encoding=UTF8_ENCODING) as json_file:
                json.dump(task_collection, json_file, indent=4)
            print(LOG_TASK_UPDATED)
            task_found = True
            break

    if not task_found:
        print(LOG_TASK_NOT_FOUND_TEMPLATE.format(task_id=task_id))


def build_task_dict(name: str, description: str, status: str):
    return {
        TASK_FIELD_NAME: name,
        TASK_FIELD_DESCRIPTION: description,
        TASK_FIELD_STATUS: status
    }


def with_created(model: Dict[str, str]):
    print(LOG_ATTACHING_CREATED_AT)
    model[TASK_FIELD_CREATED_AT] = dt.datetime.now().isoformat()
    return model


def with_updated(model: Dict[str, str]):
    print(LOG_ATTACHING_UPDATED_AT)
    model[TASK_FIELD_UPDATED_AT] = dt.datetime.now().isoformat()
    return model


def with_id(model: Dict[str, str]):
    print(LOG_ATTACHING_ID)
    model[TASK_FIELD_ID] = str(uuid.uuid4())
    return model
