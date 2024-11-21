import asyncio
import time
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.celery_conf import celery_app
from src.task_tracker.service import TaskService
from src.task_tracker.schemas import CreateTaskSchema


async def long_time_task(delay: int, session: AsyncSession, task: CreateTaskSchema) -> None:
    task_service = TaskService(session=session)
    await asyncio.sleep(delay)
    await task_service.create(task)


@celery_app.task
def dummy_task(delay:int):
    from time import sleep
    sleep(delay)
    now = datetime.now()
    return now

@celery_app.task
def test_task(arg):
    print(arg)
