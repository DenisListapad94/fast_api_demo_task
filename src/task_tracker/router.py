from fastapi import Query, Body, APIRouter, Depends
from src.task_tracker.schemas import CreateTaskSchema, ResponseTaskSchema, ResponseCommentSchema, CreateCommentsSchema
from src.task_tracker.service import TaskService, CommentService
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.orm.database import get_async_session

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "",
    description="create task",
    # response_model=ResponseTaskSchema,
    status_code=201
)
async def create_task_handler(
        task: CreateTaskSchema,
        session: AsyncSession = Depends(get_async_session)
):
    task_service = TaskService(session=session)

    return await task_service.create(task)


@router.get(
    "",
    description="get all task",
    # response_model=ResponseTaskSchema,
    status_code=200
)
async def get_tasks_handler(
        session: AsyncSession = Depends(get_async_session)
):
    task_service = TaskService(session=session)

    return await task_service.get_all()


@router.get(
    "/comment_all",
    description="get all task with comments",
    # response_model=ResponseTaskSchema,
    status_code=200
)
async def get_tasks_handler(
        session: AsyncSession = Depends(get_async_session)
):
    task_service = TaskService(session=session)

    return await task_service.get_all_comments()


@router.get(
    "/{task_id}/comment_all",
    description="gettask with comments",
    # response_model=ResponseTaskSchema,
    status_code=200
)
async def get_tasks_handler(
        task_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    task_service = TaskService(session=session)

    return await task_service.get_with_comments(task_id=task_id)


@router.get(
    "/{task_id}",
    description="get task",
    # response_model=ResponseTaskSchema,
    status_code=200
)
async def get_task_handler(
        task_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    task_service = TaskService(session=session)

    return await task_service.get(task_id=task_id)


@router.delete(
    "/{task_id}",
    description="delete task",
    # response_model=ResponseTaskSchema,
    status_code=200
)
async def delete_task_handler(
        task_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    task_service = TaskService(session=session)

    return await task_service.delete(task_id=task_id)


@router.post(
    "/comments",
    description="create comment",
    # response_model=ResponseCommentSchema,
    status_code=201
)
async def create_comment_handler(
        comment: CreateCommentsSchema,
        session: AsyncSession = Depends(get_async_session)
):
    comment_service = CommentService(session=session)

    return await comment_service.create(comment)
