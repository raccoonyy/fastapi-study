from unittest import TestCase

from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

from .cors import app


client = TestClient(app)


class TestCORS(TestCase):
    def test_사전_요청_options(self):
        headers = {
            "Origin": "https://localhost.tiangolo.com",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "X-Example",
        }

        response = client.options("/", headers=headers)
        assert response.status_code == 200
        assert response.text == "OK"
        assert response.headers["access-control-allow-origin"] == "https://localhost.tiangolo.com"
        assert response.headers["access-control-allow-headers"] == "X-Example"
    
    def test_일반_요청(self):
        headers = { "Origin": "http://localhost" }
        response = client.get("/", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Hello world"}
        assert response.headers["access-control-allow-origin"] == "http://localhost"

    def test_단순_요청_get(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello world"}
        assert "access-control-allow-origin" not in response.headers

    def test_사전_요청_실패(self):
        headers = { "Origin": "http://outside" }
        response = client.options("/", headers=headers)
        assert response.status_code == 405


# 아래는 왜 안 될까?
# class TestOtherOptions(TestCase):
#     def test_allow_methods(self):
#         app.add_middleware(
#             CORSMiddleware,
#             allow_origins=["http://localhost"],
#             allow_credentials=False,
#             allow_methods=["PATCH"],
#             allow_headers=["*"],
#         )

#         headers = { "Origin": "http://localhost" }
#         response = client.get("/", headers=headers)
#         assert response.status_code == 404
#         assert response.headers["access-control-allow-origin"] == "http://localhost"

#     def test_allow_headers(self):
#         from fastapi import FastAPI
#         fapp = FastAPI()
#         fapp.add_middleware(
#             CORSMiddleware,
#             allow_origins=["http://localhost"],
#             allow_credentials=False,
#             allow_methods=["*"],
#             allow_headers=["Access-Control-Request-Method"],
#         )
#         @fapp.get("/")
#         async def main():
#             return {"message": "Hello world"}

#         headers = { "Origin": "http://localhost" }
#         response = client.get("/", headers=headers)
#         assert response.status_code == 405
#         assert response.json() == {"message": "Hello world"}
#         assert response.headers["access-control-allow-origin"] == "http://localhost"
