from libs.domains.posts.src.collection import posts_collection
from libs.utils.db.mongoose.src.base_repository import BaseRepository


class PostsRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection=posts_collection, timestamps=True)


posts_repository = PostsRepository()
