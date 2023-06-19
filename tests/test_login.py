import pytest
from jose import jwt
from app.schemas import token_schema
from app.config import settings


def test_login(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = token_schema.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("dave@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("test@gmail.com", None, 422),
    ],
)
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": "wrongpassword"}
    )
    assert res.status_code == 403
