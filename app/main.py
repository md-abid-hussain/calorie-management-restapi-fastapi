from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .models import models
from .database import database
from .routers import user, entries, register, auth, setting
from .routers.admin_crud import entry as entry_crud, setting as setting_crud

models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(register.router)
app.include_router(auth.router)
app.include_router(entry_crud.router)
app.include_router(setting_crud.router)
app.include_router(user.router)
app.include_router(entries.router)
app.include_router(setting.router)
