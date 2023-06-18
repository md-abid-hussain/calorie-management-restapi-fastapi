from pydantic import BaseModel
from . import user_schema, setting_schema, entry_schema


class UserSettingResponse(setting_schema.SettingResponse):
    owner: user_schema.UserResponse


class UserSettingCreate(setting_schema.SettingCreate):
    pass


class UserEntriesResponse(entry_schema.EntryResponse):
    owner: user_schema.UserResponse


class EntryResponse(entry_schema.EntryResponse):
    pass


class EntryCreate(entry_schema.EntryCreate):
    pass
