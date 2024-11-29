from typing import AsyncGenerator

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm.session import Session

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SYNC_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine(ASYNC_DATABASE_URL)
sync_engine = create_engine(SYNC_DATABASE_URL)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


def get_sync_session():
    with Session(sync_engine) as session:
        yield session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
