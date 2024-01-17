from libs.domains.users.src.collection import users_collection
from libs.utils.db.mongoose.src.base_repository import BaseRepository


class UsersRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=users_collection, timestamps=True)


users_repository = UsersRepository()
