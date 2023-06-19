from app.schemas import setting_schema
import pytest


def test_unauthorized_access_setting(client):
    res = client.get("/setting/")
    assert res.status_code == 401


def test_admin_access_usersetting(authorized_admin):
    res = authorized_admin.get("/setting/")
    assert res.status_code == 403


def test_manager_access_usersetting(authorized_manager):
    res = authorized_manager.get("/setting/")
    assert res.status_code == 403


def test_get_empty_usersetting(authorized_user):
    res = authorized_user.get("/setting/")
    assert res.status_code == 404


def test_get_usersetting(authorized_user, test_setting):
    res = authorized_user.get("/setting/")
    usetting = setting_schema.SettingResponse(**res.json())
    assert usetting.user_id == test_setting.user_id
    assert usetting.expected_calories == test_setting.expected_calories
    assert res.status_code == 200


@pytest.mark.parametrize(
    "expected_calories, status_code",
    [
        (2000, 201),
        (None, 422),
    ],
)
def test_create_isvalid_usersetting(authorized_user, expected_calories, status_code):
    res = authorized_user.post(
        "/setting/", json={"expected_calories": expected_calories}
    )
    assert res.status_code == status_code


def test_create_usersetting(authorized_user):
    res = authorized_user.post("/setting/", json={"expected_calories": 2000})
    setting = setting_schema.SettingResponse(**res.json())
    assert setting.expected_calories == 2000
    assert res.status_code == 201


def test_create_usersetting_already_exists(authorized_user, test_user, test_setting):
    res = authorized_user.post(
        "/setting/", json={"user_id": test_user["id"], "expected_calories": 2000}
    )
    assert res.status_code == 400


def test_update_empty_usersetting(authorized_user):
    res = authorized_user.put(
        "/setting/", json={"user_id": 1, "expected_calories": 2000}
    )
    assert res.status_code == 400


def test_update_usersetting(authorized_user, test_user, test_setting):
    res = authorized_user.put(
        "/setting/", json={"user_id": test_user["id"], "expected_calories": 2000}
    )
    setting = setting_schema.SettingResponse(**res.json())
    assert setting.expected_calories == 2000
    assert res.status_code == 202


def test_delete_usersetting(authorized_user, test_setting):
    res = authorized_user.delete("/setting/")
    assert res.status_code == 204


def test_delete_usersetting_does_not_exist(authorized_user):
    res = authorized_user.delete("/setting/")
    assert res.status_code == 400
