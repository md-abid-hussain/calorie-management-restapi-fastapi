from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from ...database import database
from ...schemas import admin_schema
from ...models import models
from ...utils import oauth2

verify_admin = oauth2.create_role_verifier(["admin"])
router = APIRouter(
    prefix="/users", tags=["Admin CRUD settings"], dependencies=[Depends(verify_admin)]
)


@router.get("/settings", response_model=List[admin_schema.UserSettingResponse])
def get_all_users_settings(db: Session = Depends(database.get_db)):
    settings = db.query(models.UserSetting).all()
    if len(settings) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No settings found"
        )
    return settings


@router.get("/{user_id}/settings", response_model=admin_schema.UserSettingResponse)
def get_settings_by_user_id(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {user_id} does not exist",
        )
    setting = (
        db.query(models.UserSetting)
        .filter(models.UserSetting.user_id == user_id)
        .first()
    )
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Setting of user with id {user_id} not found",
        )
    return setting


@router.post(
    "/{user_id}/settings",
    status_code=status.HTTP_201_CREATED,
    response_model=admin_schema.UserSettingResponse,
)
def create_new_settings_for_user(
    user_id: int,
    setting: admin_schema.UserSettingCreate,
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {user_id} does not exist",
        )
    setting_query = (
        db.query(models.UserSetting)
        .filter(models.UserSetting.user_id == user_id)
        .first()
    )
    if setting_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Setting of user with id {user_id} already exists",
        )
    new_setting = models.UserSetting(**setting.dict(), user_id=user_id)
    db.add(new_setting)
    db.commit()
    db.refresh(new_setting)
    return new_setting


@router.put(
    "/{user_id}/settings",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=admin_schema.UserSettingResponse,
)
def update_settings_for_user(
    user_id: int,
    setting: admin_schema.UserSettingCreate,
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {user_id} does not exist",
        )
    setting_query = (
        db.query(models.UserSetting)
        .filter(models.UserSetting.user_id == user_id)
        .first()
    )
    if not setting_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Setting of user with id {user_id} does not exist",
        )
    setting_query.expected_calories = setting.expected_calories
    db.commit()
    db.refresh(setting_query)
    return setting_query


@router.delete("/{user_id}/settings", status_code=status.HTTP_204_NO_CONTENT)
def delete_settings_for_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {user_id} does not exist",
        )
    setting_query = (
        db.query(models.UserSetting)
        .filter(models.UserSetting.user_id == user_id)
        .first()
    )
    if not setting_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Setting of user with id {user_id} does not exist",
        )
    db.delete(setting_query)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
