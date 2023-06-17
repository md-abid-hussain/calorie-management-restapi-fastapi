from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import database
from ..models import models
from ..schemas import setting_schema
from ..utils import oauth2


router = APIRouter(prefix="/setting", tags=["Setting"])


@router.get("/", response_model=setting_schema.SettingResponse)
def get_setting(
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    result = (
        db.query(models.UserSetting)
        .filter(models.UserSetting.user_id == current_user.id)
        .first()
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Setting for user {current_user.id} not found",
        )
    return result


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=setting_schema.SettingResponse,
)
def create_user_setting(
    setting: setting_schema.SettingCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    setting_dict = setting.dict()
    new_setting = models.UserSetting(user_id=current_user.id, **setting_dict)
    db.add(new_setting)
    db.commit()
    db.refresh(new_setting)
    return new_setting


@router.put(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=setting_schema.SettingResponse,
)
def update_user_setting(
    setting: setting_schema.SettingCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    setting_dict = setting.dict()
    result = (
        db.query(models.UserSetting)
        .filter(models.UserSetting.user_id == current_user.id)
        .first()
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Setting for user {current_user.id} not found",
        )
    result.expected_calories = setting_dict.get("expected_calories")
    db.commit()
    db.refresh(result)
    return result


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_setting(
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    result = (
        db.query(models.UserSetting)
        .filter(models.UserSetting.user_id == current_user.id)
        .first()
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Setting for user {current_user.id} not found",
        )
    db.delete(result)
    db.commit()
    return {"detail": "Setting deleted successfully"}
