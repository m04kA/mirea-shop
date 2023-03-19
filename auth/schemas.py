import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str]
    password: Optional[str]
    email: Optional[EmailStr]
    role_id: Optional[int]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]
