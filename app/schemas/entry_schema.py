from datetime import date, time
from pydantic import BaseModel


class EntryBase(BaseModel):
    date: date | None
    time: time | None
    meal_desc: str
    calories: int | None


class EntryCreate(EntryBase):
    pass


class EntryResponse(EntryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
