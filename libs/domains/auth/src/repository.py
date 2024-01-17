from libs.domains.auth.src.collection import users_collection
from libs.util.db.mongoose.src import BaseRepository


class AuthRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=users_collection, timestamps=True)


auth_repository = AuthRepository()
