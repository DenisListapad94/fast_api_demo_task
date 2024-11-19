from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordBearer

from src.auth.authenticate import get_current_user
from src.auth.schemas import UserResponseSchema
from src.auth.models import User
from src.auth.authenticate import register
from src.auth.schemas import TokenSchema
from src.core.orm.database import get_async_session
from src.auth.schemas import UserRegisterSchema
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.authenticate import login

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post(
    "/register",
)
async def register_handler(
        user: UserRegisterSchema,
        session: AsyncSession = Depends(get_async_session)
) -> TokenSchema:
    token = await register(
        user=user,
        session=session
    )

    response = Response()
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token.access_token}",
        # httponly=True,
        # samesite="none",
        # secure=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {token.refresh_token}",
        # httponly=True,
        # samesite="none",
        # secure=True,
    )
    return token



@router.post(
    "/login",
)
async def login_handler(
        user: UserRegisterSchema,
        session: AsyncSession = Depends(get_async_session)
):
    token = await register(
        user=user,
        session=session
    )

    response = Response()
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token.access_token}",
    )
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {token.refresh_token}",
    )
    return response


@router.get(
    "/users/me",
)
async def current_user_handler(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user)
):
    return user

