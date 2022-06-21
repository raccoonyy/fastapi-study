from unittest import TestCase
from fastapi.testclient import TestClient

from main2 import app, get_current_user, User


client = TestClient(app)


class TestGetCurrentUser(TestCase):
    async def test_아무_토큰이나_넘겼을_때_사용자가_제대로_리턴되는지(self):
        user = await get_current_user("any_token")
        assert isinstance(user, User)
        assert user.email == "test@test.net"


class TestSecurityMain(TestCase):
    def test_토큰_없거나_잘못된_형태일_경우_401(self):
        response = client.get("/users/me")
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}
        assert response.headers["WWW-Authenticate"] == "Bearer"
    
        response = client.get("/users/me", headers={"Authorization": "Notexistent testtoken"})
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}
        assert response.headers["WWW-Authenticate"] == "Bearer"

    def test_토큰_형태가_정상일_때_200(self):
        response = client.get("/users/me", headers={"Authorization": "Bearer testtoken"})
        assert response.status_code == 200, response.text
        assert response.json() == {
            "username": "testtokenfakedecoded", 
            "email": "test@test.net",
            "full_name": "Alan Kim",
            "disabled": None,
        }
