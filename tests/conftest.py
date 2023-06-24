from datetime import date, time
from fastapi.testclient import TestClient
from sqlalchemy import event, Engine, create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.main import app
from app.database.database import get_db, Base
from app.utils.oauth2 import create_access_token
from app.models import models


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "testuser@mail.com", "password": "test123"}
    res = client.post("/register/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "testuser2@mail.com", "password": "test123"}
    res = client.post("/register/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token_user(test_user):
    return create_access_token({"user_id": test_user["id"], "role": "user"})


@pytest.fixture
def authorized_user(client, token_user):
    client.headers = {**client.headers, "Authorization": f"Bearer {token_user}"}
    return client


@pytest.fixture
def test_admin(client):
    user_data = {"email": "testadmin@mail.com", "password": "admin123"}
    res = client.post("/register/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token_admin(test_admin):
    return create_access_token({"user_id": test_admin["id"], "role": "admin"})


@pytest.fixture
def authorized_admin(client, token_admin):
    client.headers = {**client.headers, "Authorization": f"Bearer {token_admin}"}
    return client


@pytest.fixture
def test_manager(client):
    user_data = {"email": "testmanager@mail.com", "password": "manager123"}
    res = client.post("/register/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token_manager(test_manager):
    return create_access_token({"user_id": test_manager["id"], "role": "manager"})


@pytest.fixture
def authorized_manager(client, token_manager):
    client.headers = {**client.headers, "Authorization": f"Bearer {token_manager}"}
    return client


@pytest.fixture
def test_entries(test_user, session, test_user2):
    entries_data = [
        {
            "date": date(2021, 1, 1),
            "time": time(12, 0, 0),
            "meal_desc": "test meal 1",
            "calories": 1000,
            "user_id": test_user["id"],
        },
        {
            "date": date(2021, 1, 1),
            "time": time(12, 0, 0),
            "meal_desc": "test meal 2",
            "calories": 1500,
            "user_id": test_user["id"],
        },
        {
            "date": date(2021, 1, 1),
            "time": time(12, 0, 0),
            "meal_desc": "test meal 3",
            "calories": 2000,
            "user_id": test_user2["id"],
        },
    ]

    def create_entry_model(entry):
        return models.Entry(**entry)

    entries_map = map(create_entry_model, entries_data)
    session.add_all(list(entries_map))
    session.commit()
    return session.query(models.Entry).all()


@pytest.fixture
def test_setting(session, test_user, test_user2):
    setting1 = models.UserSetting(user_id=test_user["id"], expected_calories=2000)
    setting2 = models.UserSetting(user_id=test_user2["id"], expected_calories=2500)
    session.add_all([setting1, setting2])
    session.commit()
    return session.query(models.UserSetting).first()
