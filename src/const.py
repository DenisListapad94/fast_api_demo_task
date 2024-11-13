from enum import Enum


class TaskStatuses(Enum):
    new = "new"
    start = "start"
    process = "process"
    expired = "expired"
    finished = "finished"
