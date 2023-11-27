from libs.utils.db.connection import db

USERS_COLLECTION_NAME = "users"

posts_collection = db[USERS_COLLECTION_NAME]
