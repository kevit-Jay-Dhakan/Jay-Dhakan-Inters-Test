from pymongo import ASCENDING

from libs.domains.users.src.schema import USERS_VALIDATION_SCHEMA
from libs.utils.db.mongoose.src.connection import db

validation_options = {
    'validator': {'$jsonSchema': USERS_VALIDATION_SCHEMA},
    'validationLevel': 'strict',
    'validationAction': 'error'
}

USERS_COLLECTION_NAME = 'users'
users_collection = db[USERS_COLLECTION_NAME]

users_collection.create_index([('userId', ASCENDING)])

users_collection.database.command(
    'collMod',
    USERS_COLLECTION_NAME,
    **validation_options
)
