from unittest import TestCase

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

class TestMiddleware(TestCase):
    def test_add_process_time_header_middleware(self):
        response = client.get("/")

        assert response.status_code == 200
        assert response.headers.get("X-Process-Time")
