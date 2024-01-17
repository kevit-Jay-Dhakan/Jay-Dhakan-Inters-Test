USERS_VALIDATION_SCHEMA = {
    'bsonType': 'object',
    'required': [
        'userId',
        'firstName',
        'lastName',
        'password',
        'email',
        'privilege',
        'createdAt',
    ],
    'properties': {
        '_id': {'bsonType': 'objectId'},
        'userId': {'bsonType': 'string'},
        'firstName': {'bsonType': 'string'},
        'lastName': {'bsonType': 'string'},
        'password': {'bsonType': 'string'},
        'email': {'bsonType': 'string'},
        'privilege': {'bsonType': 'string'},
        'createdAt': {'bsonType': 'date'},
        'updatedAt': {'bsonType': 'date'},
        'tokens': {'bsonType': 'array'}
    }
}
