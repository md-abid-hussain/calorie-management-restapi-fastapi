from pydantic import BaseModel


class SettingBase(BaseModel):
    expected_calories: int


class SettingCreate(SettingBase):
    pass


class SettingResponse(SettingBase):
    user_id: int
