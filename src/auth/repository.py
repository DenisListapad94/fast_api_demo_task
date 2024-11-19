from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import UserRegisterSchema
from sqlalchemy import select

from src.auth.models import User


class UserRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_data: UserRegisterSchema) -> User:
        user = User(
            email=user_data.email,
            password=user_data.password,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_user(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)  # объект курсора
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)  # объект курсора
        return result.scalar_one_or_none()

    async def get_users(self) -> list[dict[str, Any]]:
        query = select(User)
        result = await self.session.execute(query)
        return [
            user.__dict__ for user in
            result.scalars().all()
        ]

    async def delete_by_id(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        await self.session.delete(user)
        await self.session.commit()
        return user
