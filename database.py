from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "campus_lost_found"
COLLECTION_NAME = "items"

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client[DATABASE_NAME]
items_collection = db[COLLECTION_NAME]

def test_connection():
    """Return True if MongoDB is reachable, otherwise False."""
    try:
        client.admin.command("ping")
        return True
    except (ConnectionFailure, ServerSelectionTimeoutError):
        return False
