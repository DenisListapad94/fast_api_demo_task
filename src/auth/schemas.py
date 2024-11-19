from datetime import datetime

from pydantic import BaseModel

from src.const import Roles


class BaseUserSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None


class UserRegisterSchema(BaseModel):
    email: str
    password: str


class UserResponseSchema(BaseUserSchema):
    email: str
    role: Roles | None = None
    created: datetime
    updated: datetime | None = None


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
