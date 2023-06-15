from datetime import date, time
from pydantic import BaseModel


class EntryBase(BaseModel):
    date: date
    time: time
    meal_desc: str
    calories: int


class EntryCreate(EntryBase):
    pass


class EntryResponse(EntryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
