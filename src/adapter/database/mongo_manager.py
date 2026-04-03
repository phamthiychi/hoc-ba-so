from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.common.connect_setting import settings

class MongoManager:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_DB_URI, server_api=ServerApi('1'))
        self.admin = self.client.admin

    def get_metadata_db(self):
        return self.client[settings.METADATA_MONGO_DB]

    def get_db(self, db_name: str):
        return self.client[db_name]

    def clean_metadata_db(self, collection_name):
        db = self.get_metadata_db()
        db[collection_name].delete_many({})

mongo_manager = MongoManager()