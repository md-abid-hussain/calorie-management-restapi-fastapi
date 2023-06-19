from app.schemas import admin_schema


def test_unauthorized_access_setting(client):
    res = client.get("/users/settings")
    assert res.status_code == 401


def test_user_access_usersetting(authorized_user):
    res = authorized_user.get("/users/settings")
    assert res.status_code == 403


def test_manager_access_usersetting(authorized_manager):
    res = authorized_manager.get("/users/settings")
    assert res.status_code == 403


def test_get_empty_usersetting(authorized_admin):
    res = authorized_admin.get("/users/settings")
    assert res.status_code == 404


def test_get_all_usersetting(authorized_admin, test_setting):
    res = authorized_admin.get("/users/settings")
    usettings = [admin_schema.UserSettingResponse(**setting) for setting in res.json()]
    assert res.status_code == 200
    assert len(usettings) == len(res.json())


def test_get_user_setting_by_id(authorized_admin, test_setting, test_user):
    res = authorized_admin.get(f"/users/settings/{test_user['id']}")
    assert res.status_code == 200
    setting = admin_schema.UserSettingResponse(**res.json())
    assert setting.user_id == test_setting.user_id
    assert setting.expected_calories == test_setting.expected_calories


def test_create_user_setting(authorized_admin, test_user):
    data = {"user_id": test_user["id"], "expected_calories": 2000}
    res = authorized_admin.post("/users/settings", json=data)
    assert res.status_code == 201
    setting = admin_schema.UserSettingResponse(**res.json())
    assert setting.user_id == data["user_id"]
    assert setting.expected_calories == data["expected_calories"]


def test_update_user_setting(authorized_admin, test_user, test_setting):
    data = {"expected_calories": 3000}
    res = authorized_admin.put(f"/users/settings/{test_user['id']}", json=data)
    assert res.status_code == 202
    assert res.json()["user_id"] == test_user["id"]
    assert res.json()["expected_calories"] == data["expected_calories"]


def test_update_user_setting_not_found(authorized_admin, test_user):
    data = {"expected_calories": 3000}
    res = authorized_admin.put(f"/users/settings/2432", json=data)
    assert res.status_code == 400


def test_delete_user_setting(authorized_admin, test_user, test_setting):
    res = authorized_admin.delete(f"/users/settings/{test_user['id']}")
    assert res.status_code == 204


def test_delete_user_setting_not_found(authorized_admin, test_user):
    res = authorized_admin.delete(f"/users/settings/2432")
    assert res.status_code == 400
