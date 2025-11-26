from typing import Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import MONGO_URI, MONGO_DB_NAME

_client: Optional[MongoClient] = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        try:
            _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            # Test connection
            _client.server_info()
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            raise ConnectionError(f"Failed to connect to MongoDB at {MONGO_URI}: {str(e)}")
    return _client


def get_db():
    return get_client()[MONGO_DB_NAME]


def get_collection(name: str) -> Collection:
    return get_db()[name]

