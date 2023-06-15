from fastapi import FastAPI, Depends

from .models import models
from .database import database
from .routers import user, entries, register

models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/")
def root():
    return {"status": "running"}


app.include_router(register.router)
app.include_router(user.router)
app.include_router(entries.router)
