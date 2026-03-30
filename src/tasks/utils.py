import os
import uuid
from pathlib import Path

from .constants import (
    LOCALAPPDATA_ENV,
    TASK_CLI,
    TASK_CLI_DIR,
    TASKS_JSON,
    EMPTY_JSON_LIST,
    UTF8_ENCODING,
    LOG_INVALID_STATUS
)
from .models import TaskStatus

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
