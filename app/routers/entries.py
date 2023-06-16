from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from ..database import database
from ..models import models
from ..schemas import entry_schema
from ..utils import oauth2, utils

router = APIRouter(
    prefix="/entries",
    tags=["entries"],
)


@router.get("/", response_model=List[entry_schema.EntryResponse])
def get_all_entries(
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    result = (
        db.query(models.Entry).filter(models.Entry.user_id == current_user.id).all()
    )
    return result


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=entry_schema.EntryResponse
)
def create_new_entry(
    entry: entry_schema.EntryCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    temp = entry.dict()
    print(temp)
    if temp.get("calories") is None:
        temp["calories"] = utils.get_calories(temp.get("meal_desc"))
    new_entry = models.Entry(user_id=current_user.id, **temp)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@router.get("/{entry_id}", response_model=entry_schema.EntryResponse)
def get_entry_by_id(
    entry_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
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
    entry: entry_schema.EntryCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
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
    result_query.update(entry.dict())
    db.commit()
    return result_query.first()


@router.delete("/{entry_id}")
def delete_entry(
    entry_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
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
