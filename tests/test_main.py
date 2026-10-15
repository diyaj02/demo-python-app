
from main import app


def test_app_info():
    client = app.test_client()
    response = client.get("/api/info")

    assert response.status_code == 200

    data = response.get_json()
    assert data["app_name"] == "Docker Demo App"
    assert data["status"] == "running"
    assert "python_version" in data
    assert "container_id" in data

def test_create_note_without_title():
    client = app.test_client()

    response = client.post(
        "/api/notes",
        json={"content": "Test content"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"


def test_create_note_with_empty_title():
    client = app.test_client()

    response = client.post(
        "/api/notes",
        json={"title": "   ", "content": "Test"}
    )

    assert response.status_code == 400


def test_create_note_with_invalid_content():
    client = app.test_client()

    response = client.post(
        "/api/notes",
        json={"title": "Test Note", "content": 123}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Content must be a string"


def test_update_note_without_title():
    client = app.test_client()

    response = client.put(
        "/api/notes/1",
        json={"content": "Updated content"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"