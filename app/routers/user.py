from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import user_schema
from ..models import models
from ..database import database
from ..utils import crypto

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/register", response_model=user_schema.UserResponse)
def register(user: user_schema.UserRegister, db: Session = Depends(database.get_db)):
    hashed_password = crypto.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    print(user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
