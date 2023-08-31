import os

import pytest

from fastapi.testclient import TestClient

from app.dependencies.db import MongoDatabase
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
    with TestClient(app) as client:
        yield client

    users = db.client.get_database("mt-services")[f"users:{os.getenv('UVICORN_ENV')}"]
    blacklist = db.client.get_database("mt-services")[f"blacklist:{os.getenv('UVICORN_ENV')}"]
    reports44 = db.client.get_database("test")[f"cReports44new:{os.getenv('UVICORN_ENV')}"]
    reports223 = db.client.get_database("test")[f"cReports223new:{os.getenv('UVICORN_ENV')}"]

    users.delete_many({})
    blacklist.delete_many({})
    reports44.delete_many({})
    reports223.delete_many({})

