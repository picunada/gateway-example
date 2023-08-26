"""Database module"""
import os

import pymongo
from pymongo import MongoClient

from app.config.settings import Settings, settings


class MongoDatabase:
    """Database class for mongodb"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: Settings) -> None:
        """Init database client"""
        self.client: MongoClient = pymongo.MongoClient(
            config.mongo_url,
            tls=True,
            authMechanism="SCRAM-SHA-1",
            tlsAllowInvalidHostnames=True,
            tlsCAFile=f"{os.getcwd()}/app/lib/sber.crt",
        )


async def get_database() -> MongoDatabase:
    """Injection tool"""
    return MongoDatabase(config=settings)
