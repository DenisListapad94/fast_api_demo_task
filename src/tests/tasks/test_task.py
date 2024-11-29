import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.task_tracker.repository import TaskRepository
from src.task_tracker.schemas import CreateTaskSchema
from src.tests.conftest import async_session,create_tables,create_task

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def test_create_tables(async_session: AsyncSession, create_tables):
    print('Create tables int testing database...')


@pytest.mark.asyncio
async def test_create_user(create_tables,create_task):
    import pdb;pdb.set_trace()
    assert create_task.id == 1
    assert create_task.title == "test title"
    assert create_task.description == "test description"

@pytest.mark.asyncio
async def test_create_task_router(async_client,create_tables):
    test_title = "test title"
    test_description = "test description"

    body = {
        "title" : test_title,
        "description": test_description
    }

    response = await async_client.post(
        url="/tasks",
        json=body
    )

    assert response.status_code == 201

