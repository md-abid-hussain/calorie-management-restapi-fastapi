from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from ..schemas import user_schema
from ..models import models
from ..database import database
from ..utils import oauth2, crypto
from .entry_setting_admin import setting, entry

verify_role = oauth2.create_role_verifier(["manager", "admin"])
verify_admin = oauth2.create_role_verifier(["admin"])
router = APIRouter(prefix="/users", tags=["users"])


router.include_router(
    setting.router,
    tags=["User Settings CRUD ADMIN"],
    dependencies=[Depends(verify_admin)],
)

router.include_router(
    entry.router, tags=["User Entries CRUD ADMIN"], dependencies=[Depends(verify_admin)]
)


@router.get("/", response_model=List[user_schema.UserResponse])
def get_all_user(
    db: Session = Depends(database.get_db), current_user=Depends(verify_role)
):
    users = db.query(models.User).all()
    if len(users) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
        )
    return users


@router.get("/{id}", response_model=user_schema.UserResponse)
def get_user_by_id(
    id: int = None,
    db: Session = Depends(database.get_db),
    current_user=Depends(verify_role),
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    return user


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=user_schema.UserCreateResponse,
)
def create_new_user(
    user: user_schema.UserCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(verify_role),
):
    email_query = db.query(models.User).filter(models.User.email == user.email).first()
    if email_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {user.email} already registered",
        )
    if current_user.role.value == "manager" and user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User is not an admin",
            headers={"WWW-Authenticate": "Bearer"},
        )
    hashed_password = crypto.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{id}", response_model=user_schema.UserCreateResponse)
def update_user(
    id: int,
    user: user_schema.UpdateUser,
    db: Session = Depends(database.get_db),
    current_user=Depends(verify_role),
):
    user_query = db.query(models.User).filter(models.User.id == id)
    if not user_query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {id} does not exist",
        )
    if current_user.role.value == "manager" and user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User is not an admin",
            headers={"WWW-Authenticate": "Bearer"},
        )
    hashed_password = crypto.hash(user.password)
    user.password = hashed_password
    updated_user = user_query.update(user.dict())
    db.commit()
    return user_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int, db: Session = Depends(database.get_db), current_user=Depends(verify_role)
):
    user_query = db.query(models.User).filter(models.User.id == id)
    if not user_query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {id} does not exist",
        )
    if (
        current_user.role.value == "manager"
        and user_query.first().role.value == "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User is not an admin",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_query.delete(synchronize_session="auto")
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
