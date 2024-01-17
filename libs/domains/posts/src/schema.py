POSTS_VALIDATION_SCHEMA = {
    'bsonType': 'object',
    'required': [
        'postId',
        'userOid',
        'postDescription',
        'createdAt'
    ],
    'properties': {
        '_id': {'bsonType': 'objectId'},
        'postDescription': {'bsonType': 'string'},
        'userOid': {'bsonType': 'objectId'},
        'postId': {'bsonType': 'string'},
        'createdAt': {'bsonType': 'date'},
        'updatedAt': {'bsonType': 'date'}
    }
}
