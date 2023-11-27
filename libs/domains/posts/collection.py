from libs.utils.db.connection import db

POSTS_COLLECTION_NAME = "posts"

posts_collection = db[POSTS_COLLECTION_NAME]
