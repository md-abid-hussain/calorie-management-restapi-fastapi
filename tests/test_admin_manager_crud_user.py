from app.schemas import user_schema
import pytest


def test_unauthorized_access_setting(client):
    res = client.get("/users/")
    assert res.status_code == 401


def test_user_access_usersetting(authorized_user):
    res = authorized_user.get("/users/")
    assert res.status_code == 403


def test_admin_get_all_user(authorized_admin):
    res = authorized_admin.get("/users/")
    user = [user_schema.UserResponse(**user) for user in res.json()]
    assert res.status_code == 200
    assert len(user) == len(res.json())


def test_manager_get_all_user(authorized_manager):
    res = authorized_manager.get("/users/")
    user = [user_schema.UserResponse(**user) for user in res.json()]
    assert res.status_code == 200
    assert len(user) == len(res.json())


def test_admin_get_user_by_id(test_user, authorized_admin):
    res = authorized_admin.get(f"/users/1")
    assert res.status_code == 200
    assert res.json()["id"] == test_user["id"]
    assert res.json()["email"] == test_user["email"]


def test_manager_get_user_by_id(test_user, authorized_manager):
    res = authorized_manager.get(f"/users/1")
    assert res.status_code == 200
    assert res.json()["id"] == test_user["id"]
    assert res.json()["email"] == test_user["email"]


def test_admin_get_user_id_does_not_exist(authorized_admin):
    res = authorized_admin.get("/users/999")
    assert res.status_code == 404


def test_manager_get_user_id_does_not_exist(authorized_manager):
    res = authorized_manager.get("/users/999")
    assert res.status_code == 404


@pytest.mark.parametrize(
    "email, password, role, status_code",
    [
        ("temp@mail.com", "password123", "user", 201),
        ("temp2@mail.com", "password123", "manager", 201),
        (None, "password123", "user", 422),
        ("temp3@mail.com", None, "user", 422),
        ("temp4@mail.com", "password123", None, 422),
    ],
)
def test_admin_create_user(authorized_admin, email, password, role, status_code):
    res = authorized_admin.post(
        "/users/",
        json={
            "email": email,
            "password": password,
            "role": role,
        },
    )
    assert res.status_code == status_code


@pytest.mark.parametrize(
    "email, password, role, status_code",
    [
        ("temp@mail.com", "password123", "user", 201),
        ("temp2@mail.com", "password123", "manager", 201),
        (None, "password123", "user", 422),
        ("temp3@mail.com", None, "user", 422),
        ("temp4@mail.com", "password123", None, 422),
    ],
)
def test_manager_create_user(authorized_manager, email, password, role, status_code):
    res = authorized_manager.post(
        "/users/",
        json={
            "email": email,
            "password": password,
            "role": role,
        },
    )
    assert res.status_code == status_code


def test_admin_create_user_existing_email(authorized_admin, test_user):
    res = authorized_admin.post(
        "/users/",
        json={
            "email": test_user["email"],
            "password": "password123",
            "role": "user",
        },
    )
    assert res.status_code == 400


def test_manager_create_user_existing_email(authorized_manager, test_user):
    res = authorized_manager.post(
        "/users/",
        json={
            "email": test_user["email"],
            "password": "password123",
            "role": "user",
        },
    )
    assert res.status_code == 400


def test_manager_create_admin(authorized_manager):
    res = authorized_manager.post(
        "/users/",
        json={
            "email": "man@mail.com",
            "password": "password123",
            "role": "admin",
        },
    )
    assert res.status_code == 403


def test_admin_update_user(test_user2, authorized_admin):
    res = authorized_admin.put(
        "/users/1",
        json={
            "id": 1,
            "email": "update@mail.com",
            "password": "password123",
            "role": "user",
        },
    )
    assert res.status_code == 200


def test_manager_update_user(test_user2, authorized_manager):
    res = authorized_manager.put(
        "/users/1",
        json={
            "id": 1,
            "email": "update@mail.com",
            "password": "password123",
            "role": "user",
        },
    )
    assert res.status_code == 200


def test_admin_update_user_id_does_not_exist(authorized_admin):
    res = authorized_admin.put(
        "/users/999",
        json={
            "id": 999,
            "email": "tes@mail.com",
            "password": "password123",
            "role": "user",
        },
    )
    assert res.status_code == 400


def test_manager_update_user_id_does_not_exist(authorized_manager):
    res = authorized_manager.put(
        "/users/999",
        json={
            "id": 999,
            "email": "tes@mail.com",
            "password": "password123",
            "role": "user",
        },
    )
    assert res.status_code == 400


def test_admin_delete_user(authorized_admin, test_user):
    res = authorized_admin.delete(f"/users/{test_user['id']}")
    assert res.status_code == 204


def test_manager_delete_user(authorized_manager, test_user):
    res = authorized_manager.delete(f"/users/{test_user['id']}")
    assert res.status_code == 204


def test_admin_delete_user_id_does_not_exist(authorized_admin):
    res = authorized_admin.delete("/users/999")
    assert res.status_code == 400


def test_manager_delete_user_id_does_not_exist(authorized_manager):
    res = authorized_manager.delete("/users/999")
    assert res.status_code == 400


def test_admin_delete_manager(authorized_admin, test_manager):
    res = authorized_admin.delete(f"/users/{test_manager['id']}")
    assert res.status_code == 204
