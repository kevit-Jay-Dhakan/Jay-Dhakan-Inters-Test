from pymongo import MongoClient

from libs.utils.db.config import DATABASE_NAME, DATABASE_URL

client = MongoClient(DATABASE_URL)
db = client[DATABASE_NAME]
