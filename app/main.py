from fastapi import FastAPI
from .schemas import user_schema

app = FastAPI()


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/register")
def register(user: user_schema.UserRegister):
    return user.dict()
