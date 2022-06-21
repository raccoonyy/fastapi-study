import os


import os
from pathlib import Path
from unittest import TestCase

from fastapi.testclient import TestClient

from .main2 import app

client = TestClient(app)



class Test(TestCase):
    def tearDown(self) -> None:
        log = Path("log2.txt")
        if log.is_file():
            os.remove(log)
        return super().tearDown()

    def test_main(self):
        response = client.post("/send-notification/foo@example.com?q=test-query")
        assert response.status_code == 200
        assert response.json() == {"message": "Message sent"}
        with open("./log2.txt") as f:
            assert "found query: test-query\nmessage to foo@example.com" in f.read()
