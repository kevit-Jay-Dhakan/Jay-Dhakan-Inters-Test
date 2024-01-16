from libs.domains.auth.src.collection import users_collection


class AuthRepository:
    @staticmethod
    def find_one(query=None, projection=None):
        if query is None:
            query = {}
        if projection is None:
            projection = {}

        return users_collection.find_one(query, projection)

    @staticmethod
    def update_one(query=None, projection=None):
        if query is None:
            query = {}
        if projection is None:
            projection = {}

        return users_collection.update_one(query, projection)


auth_repository = AuthRepository()
