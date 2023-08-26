from fastapi.testclient import TestClient

from app.dependencies.db import get_database
from app.dependencies.test import get_test_database
from app.main import app


app.dependency_overrides[get_database] = get_test_database

client = TestClient(app)


def test_user_creation():
    user = dict(email="test@example.com", username="test", password="password", password2="password")
    response = client.post("/api/v1/user",
                           headers={
                               'content-type': 'application/json'
                           },
                           json=user)

    assert response.status_code == 201


def test_user_creation_not_valid_email():
    user = dict(email="testcom", username="test", password="password", password2="password")
    response = client.post("/api/v1/user",
                           headers={
                               'content-type': 'application/json'
                           },
                           json=user)

    assert response.status_code == 422


def test_user_creation_passwords_not_match():
    user = dict(email="test@example.com", username="test", password="password2", password2="password")
    response = client.post("/api/v1/user",
                           headers={
                               'content-type': 'application/json'
                           },
                           json=user)

    assert response.status_code == 422
    assert "loc" in response.json()["detail"][0].keys()
    assert "Value error, Passwords do not match" == response.json()["detail"][0]['msg']
