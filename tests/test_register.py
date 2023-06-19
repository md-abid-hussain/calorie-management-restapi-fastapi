from app.schemas import user_schema


def test_register_user(client):
    res = client.post(
        "/register/", json={"email": "fast@mail.com", "password": "fast123"}
    )
    new_user = user_schema.UserBase(**res.json())
    assert new_user.email == "fast@mail.com"
    assert res.status_code == 201


def test_register_user_error(client, test_user):
    res = client.post(
        "/register/",
        json={"email": test_user["email"], "password": test_user["password"]},
    )
    assert res.status_code == 400
