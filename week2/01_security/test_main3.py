from unittest import TestCase
from fastapi.testclient import TestClient


class BaseTestCase(TestCase):
    def setUp(self):
        from main3 import app
        self.client = TestClient(app)


class TestLogin(BaseTestCase):
    def test_get_요청은_405(self):
        response = self.client.get("/token")
        assert response.status_code == 405

    def test_login_username_틀렸을_때_400(self):
        response = self.client.post("/token", data={"username": "alankim", "password": "secret"})
        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect username or password"}

    def test_login_password_틀렸을_때_400(self):
        response = self.client.post("/token", data={"username": "johndoe", "password": "idontknow"})
        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect username or password"}

    def test_login_200(self):
        response = self.client.post("/token", data={"username": "johndoe", "password": "secret"})
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "token_type" in response.json()
        

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
        assert response.json() == {"detail": "Invalid authentication credentials"}
        assert response.headers["WWW-Authenticate"] == "Bearer"

    def test_inactive_사용자는_400(self):
        response = self.client.get("/users/me", headers={"Authorization": "Bearer alice"})
        assert response.status_code == 400
        assert response.json() == {"detail": "Inactive user"}

    def test_토큰이_정상일_때(self):
        response = self.client.get("/users/me", headers={"Authorization": "Bearer johndoe"})
        assert response.status_code == 200, response.text
        assert response.json() == {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "fakehashedsecret",
            "disabled": False,
        }
