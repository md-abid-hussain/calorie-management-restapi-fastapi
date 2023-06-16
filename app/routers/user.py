from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..schemas import user_schema
from ..models import models
from ..database import database
from ..utils import oauth2

verify_role = oauth2.create_role_verifier(["manager", "admin"])
router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(verify_role)])


@router.get("/", response_model=List[user_schema.UserResponse])
def get_all_user(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{id}", response_model=user_schema.UserResponse)
def get_user_by_id(db: Session = Depends(database.get_db), id: int = None):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user
