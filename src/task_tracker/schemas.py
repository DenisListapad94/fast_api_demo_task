from datetime import datetime

from pydantic import BaseModel

from src.const import TaskStatuses



class BaseCommentSchema(BaseModel):
    comment: str
    rating: int | None = None


class CreateCommentsSchema(BaseCommentSchema):
    task_id: int


class ResponseCommentSchema(CreateCommentsSchema):
    id: int
    created: datetime
    updated: datetime | None = None

class BaseTasksSchema(BaseModel):
    title: str
    description: str


class CreateTaskSchema(BaseTasksSchema):
    pass


class ResponseTaskSchema(BaseTasksSchema):
    id: int
    created: datetime
    updated: datetime | None = None
    comments: list[ResponseCommentSchema] | None = None


class UpdateTaskSchema(BaseTasksSchema):
    pass






