from sqlalchemy import (
    TIME,
    Column,
    Integer,
    String,
    TIMESTAMP,
    text,
    DATE,
    ForeignKey,
    Enum,
)
from ..database import database
from ..schemas.user_schema import Roles


class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Roles), nullable=False, default="user")
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("(datetime('now', 'localtime'))"),
        nullable=False,
    )


class Entry(database.Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(DATE, nullable=False, server_default=text("(date('now'))"))
    time = Column(TIME, nullable=False, server_default=text("(time('now'))"))
    meal_desc = Column(String, nullable=False)
    calories = Column(Integer, nullable=False, server_default=text("0"))
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )


class UserSetting(database.Base):
    __tablename__ = "user_settings"
    id = Column(Integer, primary_key=True, nullable=False)
    expected_calories = Column(Integer, nullable=False, server_default=text("2250"))
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
