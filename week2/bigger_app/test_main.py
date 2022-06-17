from unittest import TestCase
from fastapi.testclient import TestClient
from parameterized import parameterized
from .main import app


client = TestClient(app)


no_jessica = {
    "detail": [
        {
            "loc": ["query", "token"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
}


class TestUserGetPaths(TestCase):
    @parameterized.expand([
        "/users",
        "/users/foo",
        "/users/me",
    ])
    def test_토큰_없으면_422(self, path):
        response = client.get(path, headers={})
        assert response.status_code == 422
        assert response.json() == no_jessica
    
    @parameterized.expand([
        "/users?token=monica", 
        "/users/foo?token=monica", 
        "/users/me?token=monica",
    ])
    def test_잘못된_토큰은_400(self, path):
        response = client.get(path)
        assert response.status_code == 400
        assert response.json() == {"detail": "No jessica token provided"}

    @parameterized.expand([
        ("/users?token=jessica", [{"username": "Rick"}, {"username": "Morty"}]),
        ("/users/foo?token=jessica", {"username": "foo"}),
        ("/users/me?token=jessica", {"username": "fakecurrentuser"}),
    ])
    def test_토큰이_옳다면_200(self, path, expected_response):
        response = client.get(path)
        assert response.status_code == 200
        assert response.json() == expected_response


class TestItemGetPaths(TestCase):
    def setUp(self) -> None:
        self.headers = {"X-Token": "fake-super-secret-token"}
        
    @parameterized.expand([
        "/items?token=jessica",
        "/items/plumbus?token=jessica",
    ])
    def test_헤더_없으면_422(self, path):
        expected_response = {
            "detail": [
                {
                    "loc": ["header", "x-token"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
        response = client.get(path)
        assert response.status_code == 422
        assert response.json() == expected_response
    
    @parameterized.expand([
        "/items",
        "/items/plumbus",
    ]) 
    def test_이상한_헤더는_400(self, path):
        response = client.get(path, headers={"X-Token": "invalid"})
        assert response.status_code == 400
        assert response.json() == {"detail": "X-Token header invalid"}

    @parameterized.expand([
        "/items",
        "/items/plumbus",
    ])
    def test_토큰_없으면_422(self, path):
        response = client.get(path, headers=self.headers)
        assert response.status_code == 422
        assert response.json() == no_jessica

    @parameterized.expand([
        "/items?token=jessica",
        "/items/plumbus?token=jessica",
    ])
    def test_토큰과_헤더가_옳다면_200(self, path):
        response = client.get(path, headers=self.headers)
        assert response.status_code == 200


class TestItemPut(TestCase):
    def setUp(self) -> None:
        self.url = "/items/foo"
        self.headers = {"X-Token": "fake-super-secret-token"}
        
    def test_헤더_없으면_422(self):
        expected_response = {
            "detail": [
                {
                    "loc": ["query", "token"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["header", "x-token"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
        response = client.put(self.url)
        assert response.status_code == 422
        assert response.json() == expected_response
    
    def test_이상한_헤더는_400(self):
        response = client.put(self.url, headers={"X-Token": "invalid"})
        assert response.status_code == 400
        assert response.json() == {"detail": "X-Token header invalid"}
    
    def test_권한_없는_아이템은_403(self):
        response = client.put("/items/bar?token=jessica", headers=self.headers)
        assert response.status_code == 403
        assert response.json() == {"detail": "You can only update the item: plumbus"}

    def test_200(self):
        response = client.put("/items/plumbus?token=jessica", headers=self.headers)
        assert response.status_code == 200
        assert response.json() == {"item_id": "plumbus", "name": "The great Plumbus"}


class TestMain(TestCase):
    def test_토큰_없으면_422(self):
        response = client.get("/")
        assert response.status_code == 422
        assert response.json() == no_jessica

    def test_토큰이_옳다면_200(self):
        response = client.get("/?token=jessica")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello Bigger Applications!"}


class TestAdmin(TestCase):
    def test_헤더_없으면_400(self):
        response = client.post("/admin/", headers={"X-Token": "invalid"})
        assert response.status_code == 400
        assert response.json() == {"detail": "X-Token header invalid"}

    def test_admin_200(self):
        response = client.post(
            "/admin/?token=jessica", headers={"X-Token": "fake-super-secret-token"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Admin getting schwifty"}
