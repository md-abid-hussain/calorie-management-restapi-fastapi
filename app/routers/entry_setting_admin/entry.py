from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from ...models import models
from ...database import database
from ...schemas import admin_schema

router = APIRouter()


@router.get("/entries", response_model=List[admin_schema.UserEntriesResponse])
def get_all_users_entries(db: Session = Depends(database.get_db)):
    entries = db.query(models.Entry).all()
    if len(entries) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, details="No entries found"
        )
    return entries


@router.get("/{user_id}/entries", response_model=List[admin_schema.EntryResponse])
def get_entry_of_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="User with {user_id} does not exist",
        )
    entries = db.query(models.Entry).filter(models.Entry.user_id == user_id).all()
    if len(entries) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details="No entries found for user with id {user_id}",
        )
    return entries


@router.get("/{user_id}/entries/{id}", response_model=admin_schema.EntryResponse)
def get_entry_with_id_of_user(
    user_id: int, id: int, db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="User with id {user_id} does not exist",
        )
    entry = (
        db.query(models.Entry)
        .filter(models.Entry.id == id, models.Entry.user_id == user_id)
        .first()
    )
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details="Entry with id {id} does not exist for user with id {user_id}",
        )
    return entry


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
            details="User with id {user_id} does not exist",
        )
    entry = models.Entry(**entry.dict(), user_id=user_id)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.put("/{user_id}/entries/{id}", response_model=admin_schema.EntryResponse)
def update_entry_with_id_of_user(
    user_id: int,
    id: int,
    updated_entry: admin_schema.EntryCreate,
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="User with id {user_id} does not exist",
        )
    entry_query = db.query(models.Entry).filter(
        models.Entry.id == id, models.Entry.user_id == user_id
    )
    if not entry_query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Entry with id {id} does not exist for user with id {user_id}",
        )
    entry_query.update(updated_entry.dict())
    db.commit()
    return entry_query.first()


@router.delete("/{user_id}/entries/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry_with_id_of_user(
    user_id: int, id: int, db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="User with id {user_id} does not exist",
        )
    entry_query = db.query(models.Entry).filter(
        models.Entry.id == id, models.Entry.user_id == user_id
    )
    if not entry_query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Entry with id {id} does not exist for user with id {user_id}",
        )
    entry_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{user_id}/entries", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_entries_of_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="User with id {user_id} does not exist",
        )
    entry_query = db.query(models.Entry).filter(models.Entry.user_id == user_id)
    if len(entry_query.all()) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details="No entries found for user with id {user_id}",
        )
    entry_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
