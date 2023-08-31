import os

from app.dependencies.db import MongoDatabase
from app.models.auth import Token


class Blacklist:
    @staticmethod
    def blacklist_token(db: MongoDatabase | None, token: Token) -> bool:
        assert db is not None
        # Put token in blacklist database
        blacklist = db.client.get_database("mt-services")[
            f"blacklist:{os.getenv('UVICORN_ENV')}"
        ]
        blacklist.insert_one(token.model_dump())

        return True

    @staticmethod
    def is_blacklisted(db: MongoDatabase | None, token: str) -> bool:
        assert db is not None
        # Check if token in blacklist database
        blacklist = db.client.get_database("mt-services")[
            f"blacklist:{os.getenv('UVICORN_ENV')}"
        ]
        if blacklist.find_one({"access_token": token}) or blacklist.find_one(
            {"refresh_token": token}
        ):
            return True

        return False
