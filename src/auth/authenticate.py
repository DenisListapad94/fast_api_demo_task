from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, security, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.repository import UserRepository
from src.auth.models import User

from src.auth.schemas import UserRegisterSchema, TokenSchema
from src.config import TOKEN_TYPE, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, SECRET_KEY, JWT_ALGORITHM
from src.core.orm.database import get_async_session


async def _create_token(user: User, expire_time: int, secret_key: str, token_type: str) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=int(expire_time))
    to_encode = {
        "exp": expires_delta,
        "user_id": str(user.id),
        "token_type": token_type
    }
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=secret_key,
        algorithm=JWT_ALGORITHM
    )
    return encoded_jwt


async def create_access_token(user: User) -> str:
    return await _create_token(
        user=user,
        expire_time=ACCESS_TOKEN_EXPIRE_MINUTES,
        secret_key=SECRET_KEY,
        token_type="access_token"
    )


async def create_refresh_token(user: User) -> str:
    return await _create_token(
        user=user,
        expire_time=REFRESH_TOKEN_EXPIRE_MINUTES,
        secret_key=SECRET_KEY,
        token_type="refresh_token",
    )


def verify_jwt(token_jwt: str) -> dict | None:
    try:
        split_token = token_jwt.split(" ")
        if split_token[0] != TOKEN_TYPE:
            raise HTTPException(401)

        return jwt.decode(
            split_token[-1],
            SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )
    except Exception:
        return


async def get_current_user(
        token: str = Depends(security.APIKeyCookie(name='access_token', auto_error=False)),
        session: AsyncSession = Depends(get_async_session),

):
    user_repository = UserRepository(session=session)
    payload = verify_jwt(token)

    if payload is None:
        raise HTTPException(401)

    user_id = int(payload.get("user_id"))
    user = await user_repository.get_user(user_id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_current_user_by_refresh_token(
        token: str = Depends(security.APIKeyCookie(name='refresh_token', auto_error=False)),
        session: AsyncSession = Depends(get_async_session)
):
    return await get_current_user(token=token, session=session)


async def login(user_data: UserRegisterSchema, session: AsyncSession) -> TokenSchema:
    user_repository = UserRepository(session=session)
    user = await user_repository.get_user_by_email(email=user_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if user.password != user_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = await create_access_token(user=user)
    refresh_token = await create_refresh_token(user=user)

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def refresh_access_token(user) -> TokenSchema:
    access_token = await create_access_token(user=user)
    refresh_token = await create_refresh_token(user=user)

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def register(user: UserRegisterSchema, session: AsyncSession):
    user_repository = UserRepository(session=session)
    user = await user_repository.create_user(user_data=user)

    access_token = await create_access_token(user=user)
    refresh_token = await create_refresh_token(user=user)

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )
