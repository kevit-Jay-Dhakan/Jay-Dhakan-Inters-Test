from pymongo import ASCENDING

from libs.domains.posts.src.schema import POSTS_VALIDATION_SCHEMA
from libs.utils.db.mongoose.src.connection import db

validation_options = {
    'validator': {'$jsonSchema': POSTS_VALIDATION_SCHEMA},
    'validationLevel': 'strict',
    'validationAction': 'error'
}

POSTS_COLLECTION_NAME = 'posts'
posts_collection = db[POSTS_COLLECTION_NAME]

posts_collection.create_index([('postId', ASCENDING)])
posts_collection.create_index([('userOid', ASCENDING)])

posts_collection.database.command(
    'collMod',
    POSTS_COLLECTION_NAME,
    **validation_options
)
