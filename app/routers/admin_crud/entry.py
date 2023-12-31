from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from ...models import models
from ...database import database
from ...schemas import admin_schema
from ...utils import utils
from ..entries import is_below_expected
from ...utils import oauth2

verify_admin = oauth2.create_role_verifier(["admin"])
router = APIRouter(
    prefix="/users", tags=["Admin CRUD entries"], dependencies=[Depends(verify_admin)]
)


@router.get("/entries", response_model=List[admin_schema.UserEntriesResponse])
def get_all_entries(
    db: Session = Depends(database.get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    entries = (
        db.query(models.Entry)
        .filter(models.Entry.meal_desc.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    if len(entries) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No entries found"
        )
    return entries


@router.get("/{user_id}/entries", response_model=List[admin_schema.EntryResponse])
def get_entry_of_user(
    user_id: int,
    db: Session = Depends(database.get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id, models.User.email.contains(search))
        .limit(limit)
        .offset(skip)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with {user_id} does not exist",
        )
    entries = db.query(models.Entry).filter(models.Entry.user_id == user_id).all()
    if len(entries) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No entries found for user with id {user_id}",
        )
    return entries


@router.post(
    "/{user_id}/entries",
    status_code=status.HTTP_201_CREATED,
    response_model=admin_schema.EntryResponse,
)
def create_new_entry_for_user(
    user_id: int,
    entry: admin_schema.EntryCreate,
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {user_id} does not exist",
        )
    entry_dict = entry.dict()
    if entry_dict.get("calories") == 0:
        entry_dict["calories"] = utils.get_calories(entry_dict.get("meal_desc"))
    entry_dict["below_expected"] = is_below_expected(
        user_id, entry_dict.get("date"), db
    )
    new_entry = models.Entry(**entry_dict, user_id=user_id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@router.delete("/{user_id}/entries", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_entries_of_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {user_id} does not exist",
        )
    entry_query = db.query(models.Entry).filter(models.Entry.user_id == user_id)
    if len(entry_query.all()) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No entries found for user with id {user_id}",
        )
    entry_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/entries/{id}", response_model=admin_schema.EntryResponse)
def get_entry_with_id(id: int, db: Session = Depends(database.get_db)):
    entry = db.query(models.Entry).filter(models.Entry.id == id).first()
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entry with id {id} does not exist",
        )
    return entry


@router.put("/entries/{id}", response_model=admin_schema.EntryResponse)
def update_entry_with_id(
    id: int,
    updated_entry: admin_schema.EntryCreate,
    db: Session = Depends(database.get_db),
):
    entry_query = db.query(models.Entry).filter(models.Entry.id == id)
    if not entry_query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entry with id {id} does not exist",
        )
    user_id = entry_query.first().user_id
    entry_dict = updated_entry.dict()
    if entry_dict.get("calories") == 0:
        entry_dict["calories"] = utils.get_calories(entry_dict.get("meal_desc"))
    entry_dict["below_expected"] = is_below_expected(
        user_id, entry_dict.get("date"), db
    )
    entry_dict["user_id"] = user_id
    entry_query.update(entry_dict)
    db.commit()
    return entry_query.first()


@router.delete("/entries/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry_with_id(id: int, db: Session = Depends(database.get_db)):
    entry_query = db.query(models.Entry).filter(models.Entry.id == id)
    if not entry_query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entry with id {id} does not exist",
        )
    entry_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
