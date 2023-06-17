from datetime import date, time
from pydantic import BaseModel


class EntryBase(BaseModel):
    date: date
    time: time
    meal_desc: str
    calories: int = 0


class EntryCreate(EntryBase):
    pass


class EntryResponse(EntryBase):
    id: int
    user_id: int
    below_expected: bool = True

    class Config:
        orm_mode = True
