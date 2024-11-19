from enum import Enum


class TaskStatuses(Enum):
    new = "new"
    start = "start"
    process = "process"
    expired = "expired"
    finished = "finished"


class Roles(Enum):
    user = "user"
    admin = "admin"