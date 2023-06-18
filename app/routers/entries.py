from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from ..database import database
from ..models import models
from ..schemas import entry_schema
from ..utils import oauth2, utils
from datetime import date

router = APIRouter(prefix="/entries", tags=["User CRUD Entries"])

verify_role = oauth2.create_role_verifier(["user"])


def is_below_expected(user_id: int, today: date, db: Session):
    query = (
        db.query(models.UserSetting)
        .filter(models.UserSetting.user_id == user_id)
        .first()
    )
    if not query:
        return True
    expected_calories = query.expected_calories
    total_calories = (
        db.query(models.Entry)
        .filter(models.Entry.user_id == user_id, models.Entry.date == today)
        .with_entities(models.Entry.calories)
        .all()
    )
    if not total_calories:
        return True
    total_calories = sum([i[0] for i in total_calories])
    if total_calories > expected_calories:
        return False
    return True


@router.get("/", response_model=List[entry_schema.EntryResponse])
def get_all_entries(
    db: Session = Depends(database.get_db),
    current_user=Depends(verify_role),
):
    result = (
        db.query(models.Entry).filter(models.Entry.user_id == current_user.id).all()
    )
    if len(result) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No entries found"
        )
    return result


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=entry_schema.EntryResponse
)
def create_new_entry(
    entry: entry_schema.EntryCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(verify_role),
):
    entry_dict = entry.dict()
    if entry_dict.get("calories") == 0:
        entry_dict["calories"] = utils.get_calories(entry_dict.get("meal_desc"))
    entry_dict["below_expected"] = is_below_expected(
        current_user.id, entry_dict.get("date"), db
    )
    new_entry = models.Entry(user_id=current_user.id, **entry_dict)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@router.get("/{entry_id}", response_model=entry_schema.EntryResponse)
def get_entry_by_id(
    entry_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(verify_role),
):
    result = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entry with id {entry_id} not found",
        )

    if result.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entry with id {entry_id} not found",
        )

    return result


@router.put("/{entry_id}", response_model=entry_schema.EntryResponse)
def update_entry(
    entry_id: int,
    entry: entry_schema.EntryUpdate,
    db: Session = Depends(database.get_db),
    current_user=Depends(verify_role),
):
    result_query = db.query(models.Entry).filter(models.Entry.id == entry_id)
    result = result_query.first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entry with id {entry_id} does not exist",
        )
    if result.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entry with id {entry_id} does not exist",
        )
    entry_dict = entry.dict()
    if entry_dict.get("calories") == 0:
        entry_dict["calories"] = utils.get_calories(entry_dict.get("meal_desc"))
    entry_dict["below_expected"] = is_below_expected(
        current_user.id, entry_dict.get("date"), db
    )
    result_query.update(entry_dict)
    db.commit()
    return result_query.first()


@router.delete("/{entry_id}")
def delete_entry(
    entry_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(verify_role),
):
    delete_query = db.query(models.Entry).filter(models.Entry.id == entry_id)
    result = delete_query.first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entry with id {entry_id} does not exist",
        )
    if result.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entry with id {entry_id} does not exist",
        )
    delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
