from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.MONGO_URI)

db = client[settings.DB_NAME]

questions_collection = db["questions"]
sessions_collection = db["sessions"]