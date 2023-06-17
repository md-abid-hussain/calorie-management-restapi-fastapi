from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum


class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(UserRegister):
    role: str


class UserCreateResponse(UserResponse):
    role: str


class UpdateUser(UserRegister):
    role: str


class Roles(str, Enum):
    user = "user"
    manager = "manager"
    admin = "admin"
