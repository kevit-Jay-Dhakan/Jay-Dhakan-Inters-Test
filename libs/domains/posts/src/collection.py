from libs.util.db.mongoose.src import db

POSTS_COLLECTION_NAME = "posts"

posts_collection = db[POSTS_COLLECTION_NAME]
