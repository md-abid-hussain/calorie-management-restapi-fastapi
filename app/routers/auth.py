from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import database
from ..models import models
from ..utils import oauth2, crypto
from ..schemas import token_schema

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=token_schema.Token)
def login(
    user_credential: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credential.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials"
        )

    if not crypto.verify(user_credential.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Incorrect Password"
        )
    access_token = oauth2.create_access_token(
        data={"user_id": user.id, "role": user.role.value}
    )
    return {"access_token": access_token, "token_type": "bearer"}
