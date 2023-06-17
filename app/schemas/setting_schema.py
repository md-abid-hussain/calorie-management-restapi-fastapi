from pydantic import BaseModel


class SettingBase(BaseModel):
    user_id: int
    expected_calories: int


class SettingCreate(SettingBase):
    pass


class SettingResponse(SettingBase):
    pass
