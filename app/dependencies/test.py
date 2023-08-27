"""Database module"""
import os

import gridfs
import pymongo
from pymongo import MongoClient


class MongoDatabase:
    """Database class for mongodb"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Init database client"""
        self.client: MongoClient = pymongo.MongoClient(
            os.getenv("TEST_DATABASE_URL"),
        )

        self.fs_db = self.client.reportFS
        self.report_fs = gridfs.GridFS(self.fs_db)


async def get_test_database() -> MongoDatabase:
    """Injection tool"""
    return MongoDatabase()
