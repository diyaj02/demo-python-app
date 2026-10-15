
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
