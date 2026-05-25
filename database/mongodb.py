import os
from pathlib import Path

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

class MongoDB:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        url = os.getenv("MONGODB_URL") or os.getenv("MONGO_URI")
        if not url:
            self.db = None
            return
            
        try:
            self.client = MongoClient(url, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client["ai_summarizer_db"]
            self.collection = self.db["summaries"]
        except ConnectionFailure:
            self.db = None
            print("Failed to connect to MongoDB.")
            
    def insert_summary(self, record: dict) -> str:
        if self.db is None:
            return None
        result = self.collection.insert_one(record)
        return str(result.inserted_id)
        
    def get_recent_summaries(self, limit: int = 10):
        if self.db is None:
            return []
        return list(self.collection.find().sort("created_at", -1).limit(limit))

# Singleton instance
db_instance = MongoDB()
