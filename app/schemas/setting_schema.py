from pydantic import BaseModel


class SettingBase(BaseModel):
    expected_calories: int


class SettingCreate(SettingBase):
    user_id: int


class SettingResponse(SettingBase):
    user_id: int
