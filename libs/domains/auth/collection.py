from libs.utils.db.connection import db

USERS_COLLECTION_NAME = "users"

users_collection = db[USERS_COLLECTION_NAME]
