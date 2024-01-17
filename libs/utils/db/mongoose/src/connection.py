from pymongo import MongoClient

from libs.utils.db.mongoose.src.db_config import (
    DATABASE_NAME, DATABASE_URL
)

client = MongoClient(DATABASE_URL)
db = client[DATABASE_NAME]
