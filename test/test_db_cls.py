from src.database import MongoDatabase


def test_if_singleton():
    db = MongoDatabase()

    second_db = MongoDatabase()

    assert db._instance == second_db._instance

