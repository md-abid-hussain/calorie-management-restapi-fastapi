from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import user_schema
from ..models import models
from ..database import database
from ..utils import crypto


router = APIRouter(prefix="/register", tags=["register"])


@router.post("/", response_model=user_schema.UserResponse)
def register(user: user_schema.UserRegister, db: Session = Depends(database.get_db)):
    email_query = db.query(models.User).filter(models.User.email == user.email).first()
    if email_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {user.email} already registered",
        )
    hashed_password = crypto.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
