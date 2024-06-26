"""Database module"""
import os
from typing import Any, Mapping

import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

settings: Mapping[str, Mapping[str, Any]] = {
    "prod": {
        "host": os.getenv("MONGO_URL"),
        "tls": True,
        "authMechanism": "SCRAM-SHA-1",
        "tlsAllowInvalidHostnames": True,
        "tlsCAFile": f"{os.getcwd()}/src/lib/sber.crt",
    },
    "dev": {
        "host": os.getenv("MONGO_URL"),
        "tls": True,
        "authMechanism": "SCRAM-SHA-1",
        "tlsAllowInvalidHostnames": True,
        "tlsCAFile": f"{os.getcwd()}/src/lib/sber.crt",
    },
    "test": {"host": os.getenv("TEST_DATABASE_URL")},
    "local": {"host": os.getenv("TEST_DATABASE_URL")},
}

load_dotenv()


class MongoDatabase:
    """Database class for mongodb"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        env = os.getenv("UVICORN_ENV")
        assert env is not None
        config = settings.get(env)
        print(config)
        assert config is not None

        """Init database client"""
        self.client: MongoClient = pymongo.MongoClient(**config)


async def get_database() -> MongoDatabase:
    """Injection tool"""
    return MongoDatabase()
