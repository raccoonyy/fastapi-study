import random

from fastapi.testclient import TestClient
from faker import Faker
import main

client = TestClient(main.app)
faker = Faker()


def test_root_with_dynamic_variables():
    dummy_param = {faker.word(): faker.word()}
    response = client.get("/", params=dummy_param)
    assert response.status_code == 200
    assert response.json() == dummy_param

    dummy_params = {}
    for i in range(random.randint(1, 10)):
        dummy_params.update({faker.word(): faker.word()})
    response = client.get("/", params=dummy_params)
    assert response.status_code == 200
    assert response.json() == dummy_params
