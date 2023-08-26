import pytest

from fastapi.testclient import TestClient

from app.dependencies.db import get_database
from app.dependencies.test import get_test_database, MongoDatabase
from app.main import app

db = MongoDatabase()


@pytest.fixture(scope="session")
def user():
    return dict(
        email="test@example.com",
        username="test",
        password="password",
        password2="password",
    )


@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[get_database] = get_test_database

    with TestClient(app) as client:
        yield client

    users = db.client.get_database("mt-services")["users"]
    blacklist = db.client.get_database("mt-services")["blacklist"]

    users.delete_many({"email": "test@example.com"})
    blacklist.delete_many({"token_type": "bearer"})
