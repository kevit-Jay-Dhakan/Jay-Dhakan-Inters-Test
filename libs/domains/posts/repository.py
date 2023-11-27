from libs.domains.posts.collection import posts_collection


class PostsRepository:
    @staticmethod
    def find_one(query=None, projection=None):
        if query is None:
            query = {}
        if projection is None:
            projection = {"_id": 1}
        projection["password"] = 0

        return posts_collection.find_one(query, projection)

    @staticmethod
    def insert_one(user_data: dict):
        return posts_collection.insert_one(user_data)

    @staticmethod
    def update_one(query: dict, update: dict):
        return posts_collection.update_one(query, update)

    @staticmethod
    def find_many(query=None, projection=None):
        if query is None:
            query = {}
        if projection is None:
            projection = {"_id": 1}
        projection["password"] = 0

        return posts_collection.find(query, projection)

    @staticmethod
    def delete_one(query=None):
        if query is None:
            query = {}
        return posts_collection.delete_one(query)

    @staticmethod
    def delete_many(query=None):
        if query is None:
            query = {}
        return posts_collection.delete_many(query)


posts_repository = PostsRepository()
