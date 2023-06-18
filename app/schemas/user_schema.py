from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum


class Roles(str, Enum):
    user = "user"
    manager = "manager"
    admin = "admin"


class UserBase(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    role: Roles


class UserCreate(UserRegister):
    role: Roles


class UserCreateResponse(UserResponse):
    role: Roles


class UpdateUser(UserRegister):
    role: Roles
