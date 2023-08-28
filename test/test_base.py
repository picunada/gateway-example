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
def report():
    return dict(
        active="true",
        username=True,
        db="test",
        collection="test",
        query='{"$and": [{"loadDate": {"$gte": startDate}}, {"loadDate": {"$lt": endDate}}]}',
        fields=[
            dict(
                name="regNum",
                path="regNum",
                type="str",
                description="Регистрационный номер контракта",
            )
        ],
        title="Предметы контрактов",
        subCollection=""
    )


@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[get_database] = get_test_database

    with TestClient(app) as client:
        yield client

    users = db.client.get_database("mt-services")["users"]
    blacklist = db.client.get_database("mt-services")["blacklist"]
    reports44 = db.client.get_database("test")["cReports44new"]
    reports223 = db.client.get_database("test")["cReports223new"]

    users.delete_many({})
    blacklist.delete_many({})
    reports44.delete_many({})
    reports223.delete_many({})

