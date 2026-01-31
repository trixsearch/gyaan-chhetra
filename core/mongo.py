import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoDBClient:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            mongo_uri = os.getenv("MONGO_URI")
            cls._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

            # Validate connection
            try:
                cls._client.admin.command("ping")
            except ConnectionFailure:
                raise Exception("❌ MongoDB connection failed")

        return cls._client

    @classmethod
    def get_db(cls):
        db_name = os.getenv("MONGO_DB_NAME")
        return cls.get_client()[db_name]
