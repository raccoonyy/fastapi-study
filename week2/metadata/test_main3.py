from fastapi.testclient import TestClient

from .main3 import app

client = TestClient(app)


def test_openapi_schema():
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    assert response.json()["openapi"] == "3.0.2"


def test_swagger_url():
    response = client.get("/documentation")
    assert response.status_code == 200
    assert "swagger-ui" in response.text


def test_redoc_url():
    response = client.get("/redoc")
    assert response.status_code == 404
