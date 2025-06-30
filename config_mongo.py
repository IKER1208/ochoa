import pymongo
from pymongo.errors import ConnectionFailure

MONGO_URI = "mongodb+srv://admin:admin@myatlasclusteredu.oh7cbmy.mongodb.net/"  # Cambia esto si tu URI es diferente
DB_NAME = "escuela"

client = None

def get_client():
    global client
    if client is None:
        try:
            client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
            client.admin.command('ping')
        except ConnectionFailure:
            client = None
    return client

def is_connected():
    try:
        c = get_client()
        if c is None:
            return False
        c.admin.command('ping')
        return True
    except Exception:
        return False

def get_collection(collection_name):
    c = get_client()
    if c:
        db = c[DB_NAME]
        return db[collection_name]
    return None 