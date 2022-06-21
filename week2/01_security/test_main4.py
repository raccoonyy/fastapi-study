from datetime import datetime, timedelta
from unittest import TestCase

from fastapi.testclient import TestClient
from freezegun import freeze_time
from jose import jwt


def get_access_token(
    *, username="johndoe", password="secret", scope=None, client: TestClient
):
    data = {"username": username, "password": password}
    if scope:
        data["scope"] = scope
    response = client.post("/token", data=data)
    content = response.json()
    access_token = content.get("access_token")
    return access_token


class BaseTestCase(TestCase):
    def setUp(self):
        from main4 import app
        self.client = TestClient(app)


class TestLogin(BaseTestCase):
    def test_get_요청은_405(self):
        response = self.client.get("/token")

        assert response.status_code == 405

    def test_login_username_틀렸을_때_401(self):
        response = self.client.post("/token", data={"username": "alankim", "password": "secret"})

        assert response.status_code == 401
        assert response.json() == {"detail": "Incorrect username or password"}

    def test_login_password_틀렸을_때_400(self):
        response = self.client.post("/token", data={"username": "johndoe", "password": "idontknow"})

        assert response.status_code == 401
        assert response.json() == {"detail": "Incorrect username or password"}

    def test_login_200(self):
        response = self.client.post("/token", data={"username": "johndoe", "password": "secret"})

        assert response.status_code == 200
        content = response.json()
        assert "access_token" in content
        assert content["token_type"] == "bearer"


class TestUsersMe(BaseTestCase):
    def test_토큰_없을_때_401(self):
        response = self.client.get("/users/me")

        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}
        assert response.headers["WWW-Authenticate"] == "Bearer"
    
    def test_잘못된_토큰_타입도_401(self):
        response = self.client.get("/users/me", headers={"Authorization": "Without bearer"})

        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}
        assert response.headers["WWW-Authenticate"] == "Bearer"

    def test_잘못된_토큰은_401(self):
        response = self.client.get("/users/me", headers={"Authorization": "Bearer wrong_token"})

        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}
        assert response.headers["WWW-Authenticate"] == "Bearer"
    
    def test_만료된_토큰은_401(self):
        access_token = get_access_token(scope="me", client=self.client)
        with freeze_time(datetime.utcnow() + timedelta(minutes=31)):
            response = self.client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})

        assert response.status_code == 401
    
    # scope 검사는 Advanced User Guide에서
    # def test_scope없는_토큰은_401(self):
    #     access_token = get_access_token(client=self.client)
    #     response = self.client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})

    #     assert response.status_code == 401
    #     assert response.json() == {"detail": "Not enough permissions"}
    
    def test_토큰이_정상일_때(self):
        access_token = get_access_token(scope="me", client=self.client)
        response = self.client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})

        assert response.status_code == 200
        assert response.json() == {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "disabled": False,
        }


class TestItems(BaseTestCase):
    def test_read_items(self):
        access_token = get_access_token(scope="me items", client=self.client)
        response = self.client.get("/users/me/items/", headers={"Authorization": f"Bearer {access_token}"})

        assert response.status_code == 200
        assert response.json() == [{"item_id": "Foo", "owner": "johndoe"}]

def test_verify_password():
    from main4 import fake_users_db, verify_password

    assert verify_password("secret", fake_users_db["johndoe"]["hashed_password"])


def test_get_password_hash():
    from main4 import get_password_hash

    assert get_password_hash("secretalice")


def test_create_access_token():
    from main4 import create_access_token, SECRET_KEY, ALGORITHM

    access_token = create_access_token(data={"data": "foo"})

    assert access_token
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("data") == "foo"

