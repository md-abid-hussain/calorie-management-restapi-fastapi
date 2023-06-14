from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .schemas import user_schema
from .models import models
from .database import database

models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/register")
def register(user: user_schema.UserRegister, db: Session = Depends(database.get_db)):
    new_user = models.User(**user.dict())
    print(user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
