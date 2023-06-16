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


class Roles(str, Enum):
    user = "user"
    manager = "manager"
    admin = "admin"
