from fastapi.testclient import TestClient

from sources import main
from .factories import UserFactory

client = TestClient(main.app)


def test_get_users(session):
    UserFactory.create_batch(10)

    response = client.get("/", headers={"USER-TOKEN": "dummy_token"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10


def test_me():
    user = UserFactory()

    response = client.get("/me", headers={"USER-TOKEN": user.access_token})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 0
    assert data["name"] == user.name


def test_permission():
    response = client.get("/")
    assert response.status_code == 422  # Validation Error

    response = client.get("/me")
    assert response.status_code == 422  # Validation Error
