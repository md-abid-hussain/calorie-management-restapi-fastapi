from pydantic import BaseSettings


class Settings(BaseSettings):
    SQLITE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    CALORIES_URL: str
    APP_ID: str
    API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
