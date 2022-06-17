import os


import os
from pathlib import Path
from unittest import TestCase

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)



class Test(TestCase):
    def tearDown(self) -> None:
        log = Path("log.txt")
        if log.is_file():
            os.remove(log)
        return super().tearDown()

    def test_main(self):
        response = client.post("/send-notification/foo@example.com")
        assert response.status_code == 200
        assert response.json() == {"message": "Noti sent in the background"}
        with open("./log.txt") as f:
            assert "notification for foo@example.com: some noti" in f.read()
