from unittest import TestCase
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "security": [{"OAuth2PasswordBearer": []}],
            }
        }
    },
    "components": {
        "securitySchemes": {
            "OAuth2PasswordBearer": {
                "type": "oauth2",
                "flows": {"password": {"scopes": {}, "tokenUrl": "token"}},
            }
        }
    },
}


class TestSecurityMain(TestCase):
    def test_openapi_url(self):
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert response.json() == openapi_schema

    def test_토큰_없거나_잘못된_형태일_경우_401(self):
        response = client.get("/items")
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}
        assert response.headers["WWW-Authenticate"] == "Bearer"
    
        response = client.get("/items", headers={"Authorization": "Notexistent testtoken"})
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}
        assert response.headers["WWW-Authenticate"] == "Bearer"

    def test_토큰_형태가_정상일_때_200(self):
        response = client.get("/items", headers={"Authorization": "Bearer testtoken"})
        assert response.status_code == 200, response.text
        assert response.json() == {"token": "testtoken"}
