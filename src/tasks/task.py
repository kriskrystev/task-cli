import datetime as dt
import json
import uuid
from typing import Dict

import typer
from typing_extensions import Annotated

from .constants import (
    UTF8_ENCODING,
    TASK_FIELD_ID,
    TASK_FIELD_NAME,
    TASK_FIELD_DESCRIPTION,
    TASK_FIELD_STATUS,
    TASK_FIELD_CREATED_AT,
    TASK_FIELD_UPDATED_AT,
    HELP_NAME,
    HELP_DESCRIPTION,
    HELP_STATUS,
    HELP_TASK_ID,
    HELP_UPDATE_NAME,
    HELP_UPDATE_DESCRIPTION,
    HELP_UPDATE_STATUS,
    LOG_INITIAL_LOAD,
    LOG_BUILDING_TASK,
    LOG_APPENDING_TASK,
    LOG_DUMPING_TO_JSON,
    LOG_TASK_CREATED,
    LOG_ATTACHING_CREATED_AT,
    LOG_ATTACHING_UPDATED_AT,
    LOG_ATTACHING_ID,
    LOG_LISTING_TASKS,
    LOG_TASK_DELETED,
    LOG_DELETING_TASK,
    LOG_INVALID_TASK_ID,
    LOG_TASK_NOT_FOUND_TEMPLATE,
    LOG_UPDATING_TASK,
    LOG_TASK_UPDATED,
    LOG_NO_FIELDS_TO_UPDATE,
)
from .utils import get_data_file_path, is_valid_uuid4, validate_status

DATA_TASKS_JSON = get_data_file_path()

with DATA_TASKS_JSON.open("r", encoding=UTF8_ENCODING) as json_data:
    print(LOG_INITIAL_LOAD)
    task_collection = json.load(json_data)


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
