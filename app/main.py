from fastapi import FastAPI
from .schemas import user_schema
from .models import models
from .database import database

models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/register")
def register(user: user_schema.UserRegister):
    return user.dict()
