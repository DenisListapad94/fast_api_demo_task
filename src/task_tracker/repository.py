from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.task_tracker.schemas import (
    CreateTaskSchema,
    CreateCommentsSchema,
    ResponseTaskSchema
)
from src.task_tracker.models import Tasks
from sqlalchemy import select

from src.task_tracker.models.models import Comment


class TaskRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task_data: CreateTaskSchema) -> Tasks:
        task = Tasks(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def get_task(self, task_id: int) -> Tasks:
        query = select(Tasks).where(Tasks.id == task_id)
        result = await self.session.execute(query)  # объект курсора
        return result.scalar_one_or_none()

    async def get_task_comment(self, task_id: int) -> Tasks:
        query = (select(Tasks)
                 .options(selectinload(Tasks.comments))
                 .where(Tasks.id == task_id)
                 )
        result = await self.session.execute(query)  # объект курсора
        return result.scalar_one_or_none()

    async def get_tasks(self) -> list[dict[str, Any]]:
        query = select(Tasks)
        result = await self.session.execute(query)
        return [
            task.__dict__ for task in
            result.scalars().all()
        ]

    async def get_task_with_comments(self):
        query = select(Tasks).options(selectinload(Tasks.comments))
        result = await self.session.execute(query)
        data = result.scalars().all()
        return data

    async def delete_by_id(self, task_id: int) -> Tasks:
        query = select(Tasks).where(Tasks.id == task_id)
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()
        await self.session.delete(task)
        await self.session.commit()
        return task


class CommentRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_comment(self, comment_data: CreateCommentsSchema) -> Comment:
        comment = Comment(
            comment=comment_data.comment,
            rating=comment_data.rating,
            task_id=comment_data.task_id
        )
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)

        return comment

    async def get_comment(self, comment_id: int) -> Comment:
        query = select(Comment).where(Comment.id == comment_id)
        result = await self.session.execute(query)  # объект курсора
        return result.scalar_one_or_none()

    async def get_comments(self) -> list[dict[str, Any]]:
        query = select(Comment)
        result = await self.session.execute(query)
        return [
            comment.__dict__ for comment in
            result.scalars().all()
        ]
