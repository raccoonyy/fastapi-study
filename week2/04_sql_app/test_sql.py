import importlib
import os
from pathlib import Path
from unittest import TestCase

import pytest
from fastapi.testclient import TestClient

from . import models, database


class BaseTestCase(TestCase):
    # unittest.TestCase 형태를 쓰려면, 
    # fixture도 TestCase 안에 정의해야 한다!
    @pytest.fixture(autouse=True)
    def client(self, tmp_path_factory: pytest.TempPathFactory):
        models.Base.metadata.create_all(bind=database.engine)
        
        tmp_path = tmp_path_factory.mktemp("data")
        cwd = os.getcwd()
        os.chdir(tmp_path)
        print("tmp_path", tmp_path)
        print("cwd", cwd)
        test_db = Path("./sql_app.db")
        if test_db.is_file():
            test_db.unlink()
        
        from . import main
        importlib.reload(main)
        with TestClient(main.app) as c:
            self.client = c
        if test_db.is_file():
            test_db.unlink()
        os.chdir(cwd)

    def tearDown(self):
        models.Base.metadata.drop_all(bind=database.engine)


class TestCRUD(BaseTestCase):
    def setUp(self):
        self.exists_user = {"email": "exists@test.net", "password": "password"}
        self.client.post("/users/", json=self.exists_user)

    def test_create_user(self):
        test_user = {"email": "test@test.net", "password": "password"}
        response = self.client.post("/users/", json=test_user)

        print(response.json())
        assert response.status_code == 200
        data= response.json()
        assert data["email"] == test_user["email"]
        assert "id" in data

        # 중복 생성은 안 됨
        response = self.client.post("/users/", json=test_user)
        assert response.status_code == 400
    
    def test_get_user(self):
        response = self.client.get("/users/1")

        assert response.status_code == 200
        data = response.json()
        for key in ["email", "id"]:
            with self.subTest(key=key):
                assert key in data
    
    def test_get_user_404_not_found(self):
        response = self.client.get("/users/999")

        assert response.status_code == 404
    
    def test_get_users(self):
        response = self.client.get("/users/")

        assert response.status_code == 200
        data = response.json()
        for key in ["email", "id"]:
            with self.subTest(key=key):
                assert key in data[0]


class TestItem(BaseTestCase):
    def setUp(self):
        self.test_user = {"email": "test@test.net", "password": "password"}
        self.client.post("/users/", json=self.test_user)
        self.test_item = {"title": "Foo", "description": "Something that fights"}

    def test_create_item(self):
        response = self.client.post("/users/1/items/", json=self.test_item)
        
        item_data = response.json()
        assert item_data["title"] == self.test_item["title"]
        assert item_data["description"] == self.test_item["description"]
        assert "id" in item_data
        assert "owner_id" in item_data

    def test_생성한_아이템이_사용자_상세_정보에_들어_있음(self):
        response = self.client.post("/users/1/items/", json=self.test_item)
        item_data = response.json()

        response = self.client.get("/users/1")
        user_data = response.json()
        for item in user_data["items"]:
            with self.subTest(item=item):
                if item["id"] == item_data["id"]:
                    assert item["title"] == item_data["title"]
                    assert item["description"] == item_data["description"]
    
    def test_read_items(self):
        self.client.post("/users/1/items/", json=self.test_item)
        response = self.client.get("/items/")

        assert response.status_code == 200
        data = response.json()
        assert data
        assert data[0]["title"] == self.test_item["title"]
        assert data[0]["description"] == self.test_item["description"]
