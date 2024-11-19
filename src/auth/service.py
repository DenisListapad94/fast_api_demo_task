from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.repository import UserRepository

from src.auth.models import User
from src.auth.schemas import UserRegisterSchema


class TaskService():
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UserRepository(session=session)

    async def create(self, user: UserRegisterSchema) -> User:
        return await self.repository.create_user(user_data=user)

    async def get(self, user_id: int) -> User | None:
        return await self.repository.get_user(user_id=user_id)

    async def get_all(self) -> list[dict[str, Any]]:
        return await self.repository.get_users()

    async def delete(self, user_id: int) -> User | None:
        return await self.repository.delete_by_id(user_id=user_id)
