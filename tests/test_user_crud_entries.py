import pytest
from app.schemas import entry_schema
from datetime import date, time


def test_unauthorized_access(client):
    res = client.get("/entries/")
    assert res.status_code == 401


def test_admin_access(authorized_admin):
    res = authorized_admin.get("/entries/")
    assert res.status_code == 403


def test_manager_access(authorized_manager):
    res = authorized_manager.get("/entries/")
    assert res.status_code == 403


def test_get_empty_entries(authorized_user):
    res = authorized_user.get("/entries/")
    assert res.status_code == 404


def test_get_all_entries(authorized_user, test_entries):
    res = authorized_user.get("/entries/")
    entries = [entry_schema.EntryResponse(**entry) for entry in res.json()]
    assert res.status_code == 200
    assert len(entries) == len(res.json())


def test_get_entry_by_id(authorized_user, test_entries):
    res = authorized_user.get(f"/entries/{test_entries[0].id}")
    assert res.status_code == 200
    assert res.json()["id"] == test_entries[0].id
    assert res.json()["date"] == date.isoformat(test_entries[0].date)
    assert res.json()["time"] == time.isoformat(test_entries[0].time)
    assert res.json()["user_id"] == test_entries[0].user_id
    assert res.json()["meal_desc"] == test_entries[0].meal_desc
    assert res.json()["calories"] == test_entries[0].calories
    assert res.json()["below_expected"] == test_entries[0].below_expected


def test_get_entry_id_does_not_exist(authorized_user, test_entries):
    res = authorized_user.get("/entries/999")
    assert res.status_code == 404
    assert res.json()["detail"] == "Entry with id 999 not found"


@pytest.mark.parametrize(
    "date, time, meal_desc, calories, status_code",
    [
        ("2021-01-01", "12:00:00", "test meal 1", 1000, 201),
        ("2021-01-01", "12:00:00", "test meal 2", 1500, 201),
        ("2021-01-01", "12:00:00", "test meal 3", 2000, 201),
        (None, "12:00:00", "test meal 4", 2500, 422),
        ("2021-01-01", None, "test meal 5", 3000, 422),
        ("2021-01-01", "12:00:00", None, 3500, 422),
        ("2021-01-01", "12:00:00", "test meal 6", None, 422),
    ],
)
def test_create_entries(authorized_user, date, time, meal_desc, calories, status_code):
    res = authorized_user.post(
        "/entries/",
        json={"date": date, "time": time, "meal_desc": meal_desc, "calories": calories},
    )
    assert res.status_code == status_code


def test_delete_entry_by_id(authorized_user, test_entries):
    res = authorized_user.delete(f"/entries/{test_entries[0].id}")
    assert res.status_code == 204


def test_delete_entry_id_does_not_exist(authorized_user, test_entries):
    res = authorized_user.delete("/entries/999")
    assert res.status_code == 400


def test_delete_not_owned_entry(authorized_user, test_entries):
    res = authorized_user.delete(f"/entries/{test_entries[len(test_entries)-1].id}")
    assert res.status_code == 400


def test_update_entries_by_id(authorized_user, test_entries):
    res = authorized_user.put(
        f"/entries/{test_entries[0].id}",
        json={"date": "2023-01-01", "time": "12:00:00", "meal_desc": "meal is awesome"},
    )
    updated_entry = entry_schema.EntryResponse(**res.json())
    assert updated_entry.date == date.fromisoformat("2023-01-01")
    assert updated_entry.time == time.fromisoformat("12:00:00")
    assert updated_entry.meal_desc == "meal is awesome"
    assert updated_entry.calories == 0
    assert updated_entry.below_expected == True
    assert res.status_code == 200


def test_update_entry_id_does_not_exist(authorized_user, test_entries):
    res = authorized_user.put(
        "/entries/999",
        json={"date": "2023-01-01", "time": "12:00:00", "meal_desc": "meal is awesome"},
    )
    assert res.status_code == 400
