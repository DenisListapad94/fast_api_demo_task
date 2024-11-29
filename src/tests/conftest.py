import asyncio

import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from httpx import AsyncClient, ASGITransport
from sqlalchemy.orm import sessionmaker
import asyncpg

from src.core.orm.database import get_async_session
from src.config import DB_HOST, DB_PASS, DB_PORT, DB_USER, DB_TEST_NAME, BASE_URL

from src.core.orm.base import Base
from src.task_tracker.models import Tasks

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.task_tracker.repository import TaskRepository
from src.task_tracker.schemas import CreateTaskSchema

TEST_ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_TEST_NAME}"
async_test_engine = create_async_engine(TEST_ASYNC_DATABASE_URL)
SYNC_TEST_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_TEST_NAME}"

sync_test_engine = create_engine(SYNC_TEST_DATABASE_URL)

async_test_session_maker = async_sessionmaker(async_test_engine, expire_on_commit=False)

from src.main import app


# @pytest_asyncio.fixture
# async def async_client():
#     async with AsyncClient(
#             transport=ASGITransport(app=app),
#             base_url=BASE_URL
#     ) as client:
#         yield client


@pytest_asyncio.fixture(scope="session")
async def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def create_if_not_exists():
    try:
        await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_TEST_NAME,
        )
    except asyncpg.InvalidCatalogNameError:
        sys_conn = await asyncpg.connect(
            host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{DB_TEST_NAME}" OWNER "{DB_USER}"'
        )
        await sys_conn.close()


@pytest_asyncio.fixture(scope='function')
async def create_tables():
    # await create_if_not_exists()
    Base.metadata.create_all(sync_test_engine)
    yield
    Base.metadata.drop_all(sync_test_engine)


@pytest_asyncio.fixture(scope='function')
async def async_session() -> AsyncSession:  # type: ignore
    async with async_test_session_maker() as session:
        yield session
    await async_test_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def create_task(async_session) -> Tasks:
    test_title = "test title"
    test_description = "test description"
    repository = TaskRepository(session=async_session)
    task_data = CreateTaskSchema(
        title=test_title,
        description=test_description
    )
    task = await repository.create_task(task_data=task_data)
    yield task
    await repository.delete_by_id(task_id=task.id)


@pytest_asyncio.fixture(scope="function")
async def async_client(async_session):


    app.dependency_overrides[get_async_session] = async_session
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=BASE_URL
    ) as client:
        yield client
    app.dependency_overrides.clear()

