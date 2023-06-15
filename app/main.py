from fastapi import FastAPI, Depends

from .models import models
from .database import database
from .routers import user

models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/")
def root():
    return {"status": "running"}


app.include_router(user.router)
