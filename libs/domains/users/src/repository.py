from libs.domains.users.src.collection import users_collection
from libs.util.db.mongoose.src import BaseRepository


class UsersRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=users_collection, timestamps=True)


users_repository = UsersRepository()
