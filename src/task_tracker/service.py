from typing import List, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from src.task_tracker.repository import TaskRepository, CommentRepository
from src.task_tracker.schemas import CreateTaskSchema, ResponseTaskSchema
from src.task_tracker.models import Tasks
from src.task_tracker.models.models import Comment
from src.task_tracker.schemas import CreateCommentsSchema


class TaskService():
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = TaskRepository(session=session)

    async def create(self, task: CreateTaskSchema) -> Tasks:
        return await self.repository.create_task(task_data=task)

    async def get(self, task_id: int) -> Tasks | None:
        return await self.repository.get_task(task_id=task_id)

    async def get_with_comments(self, task_id: int) -> Tasks | None:
        return await self.repository.get_task_comment(task_id=task_id)

    async def get_all(self) -> list[dict[str, Any]]:
        return await self.repository.get_tasks()

    async def get_all_comments(self):
        return await self.repository.get_task_with_comments()

    async def delete(self, task_id: int) -> Tasks | None:
        return await self.repository.delete_by_id(task_id=task_id)


class CommentService():
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = CommentRepository(session=session)

    async def create(self, comment: CreateCommentsSchema) -> Comment:
        return await self.repository.create_comment(comment_data=comment)

    async def get(self, comment_id: int) -> Comment | None:
        return await self.repository.get_comment(comment_id=comment_id)

    async def get_all(self) -> list[dict[str, Any]]:
        return await self.repository.get_comments()

