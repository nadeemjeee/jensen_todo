import pytest
from fastapi.testclient import TestClient
from app.services import file_service


@pytest.fixture
def client(tmp_path):
    """
    Use a TEMPORARY db.json for all tests.
    This prevents tests from touching your real app/data/db.json.
    """
    file_service.FILE_PATH = tmp_path / "db.json"
    from app.main import app  # import after we pointed FILE_PATH
    return TestClient(app)


def test_list_empty(client: TestClient):
    res = client.get("/todos")
    assert res.status_code == 200
    assert res.json() == []


def test_create_todo(client: TestClient):
    payload = {"title": "Test", "description": "Desc", "completed": False}
    res = client.post("/todos", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["id"] == 1
    assert data["title"] == "Test"
    assert data["completed"] is False

    # list should now contain one item
    res2 = client.get("/todos")
    assert res2.status_code == 200
    assert len(res2.json()) == 1


def test_get_todo_by_id(client: TestClient):
    client.post("/todos", json={"title": "A", "description": "", "completed": False})
    res = client.get("/todos/1")
    assert res.status_code == 200
    assert res.json()["id"] == 1


def test_get_nonexistent_todo(client: TestClient):
    res = client.get("/todos/999")
    assert res.status_code == 404
    assert res.json()["detail"] == "Todo not found"


def test_update_todo(client: TestClient):
    client.post("/todos", json={"title": "Old", "description": "", "completed": False})
    payload = {"title": "New", "description": "Updated", "completed": True}
    res = client.put("/todos/1", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == 1
    assert data["title"] == "New"
    assert data["description"] == "Updated"
    assert data["completed"] is True


def test_delete_todo(client: TestClient):
    client.post("/todos", json={"title": "To remove", "description": "", "completed": False})
    res = client.delete("/todos/1")
    assert res.status_code == 200
    assert res.json()["message"] == "Todo 1 deleted"

    # confirm it's gone
    res2 = client.get("/todos/1")
    assert res2.status_code == 404
