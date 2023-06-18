from pydantic import BaseModel
from . import user_schema, setting_schema, entry_schema


class UserSettingResponse(setting_schema.SettingResponse):
    owner: user_schema.UserResponse


class UserSettingCreate(setting_schema.SettingCreate):
    pass
