from sqlalchemy import (
    TIME,
    Column,
    Integer,
    Boolean,
    String,
    TIMESTAMP,
    text,
    DATE,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from ..database.database import Base
from ..schemas.user_schema import Roles


class User(Base):
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


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(DATE, nullable=False, server_default=text("(date('now'))"))
    time = Column(TIME, nullable=False, server_default=text("(time('now'))"))
    meal_desc = Column(String, nullable=False)
    calories = Column(Integer, nullable=False, server_default=text("0"))
    below_expected = Column(Boolean, nullable=False, server_default=text("true"))
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("User")


class UserSetting(Base):
    __tablename__ = "user_settings"
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    expected_calories = Column(Integer, nullable=False, server_default=text("2250"))
    owner = relationship("User")
