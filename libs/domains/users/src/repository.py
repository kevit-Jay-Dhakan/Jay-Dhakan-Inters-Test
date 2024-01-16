from libs.domains.users.src.collection import users_collection


class UsersRepository:
    @staticmethod
    def find_one(query=None, projection=None):
        if query is None:
            query = {}
        if projection is None:
            projection = {"_id": 1}
        projection["password"] = 0

        return users_collection.find_one(query, projection)

    @staticmethod
    def insert_one(user_data: dict):
        return users_collection.insert_one(user_data)

    @staticmethod
    def update_one(query: dict, update: dict):
        return users_collection.update_one(query, update)

    @staticmethod
    def find_many(query=None, projection=None):
        if query is None:
            query = {}
        if projection is None:
            projection = {"_id": 1}
        projection["password"] = 0

        return users_collection.find(query, projection)

    @staticmethod
    def delete_one(query=None):
        if query is None:
            query = {}
        return users_collection.delete_one(query)


users_repository = UsersRepository()
