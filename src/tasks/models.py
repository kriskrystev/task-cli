from enum import Enum

# =========================
# Task status enum
# =========================
class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW"
    DONE = "DONE"

DEFAULT_STATUS = TaskStatus.TODO
