import pytest
from fastapi.testclient import TestClient
from app.services import file_service


@pytest.fixture
def client(tmp_path):
    # Use a temporary db.json so tests don't touch your real data
    file_service.FILE_PATH = tmp_path / "db.json"
    from app.main import app
    return TestClient(app)


def test_list_empty(client: TestClient):
    res = client.get("/todos")
    assert res.status_code == 200
    assert res.json() == []


def test_create_todo(client: TestClient):
    new_todo = {
        "id": 0,
        "title": "Test Todo",
        "description": "Testing creation",
        "completed": False
    }
    res = client.post("/todos", json=new_todo)
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Test Todo"
    assert data["completed"] is False
    assert "id" in data


def test_get_todo_by_id(client: TestClient):
    res = client.get("/todos/1")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == 1
    assert data["title"] == "Test Todo"


def test_update_todo(client: TestClient):
    updated_todo = {
        "id": 1,
        "title": "Updated Todo",
        "description": "Updated",
        "completed": True
    }
    res = client.put("/todos/1", json=updated_todo)
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == 1
    assert data["title"] == "Updated Todo"
    assert data["description"] == "Updated"
    assert data["completed"] is True


def test_delete_todo(client: TestClient):
    # create something to delete (id will be 2 if previous tests ran)
    client.post("/todos", json={"id": 0, "title": "To remove", "description": "", "completed": False})

    res = client.delete("/todos/2")
    assert res.status_code == 200
    assert res.json()["message"] == "Todo 2 deleted successfully"

    # confirm it's gone
    res2 = client.get("/todos/2")
    assert res2.status_code == 404
