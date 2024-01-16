from libs.util.db.mongoose.src import BaseRepository
from libs.util.queues.src.collection_queue import CollectionQueue


class DownloadQueue(CollectionQueue):
    def __init__(self, initialize=False, repository: BaseRepository = None):
        if initialize:
            self.pause_dequeue = False
            self.repository = repository
            document_list = [
                filter_download_request(doc) for doc in
                repository.find(
                    {'download': False, 'upload': False, 'callback': False}
                )
            ]
            super().__init__(document_list=document_list)
        else:
            super().__init__(document_list=[])

    def add_downloadable(self, item):
        return self.enqueue(item)

    def get_downloadable(self):
        if not self.pause_dequeue:
            return self.dequeue()

    def get_length(self):
        return len(list(self.document))

    def get_list(self):
        return list(self.document)


def filter_download_request(document) -> dict:
    return {
        'id': document['id'],
        '_id': str(document['_id']),
        'visitorUrl': document['visitorUrl'],
        'handler_profile_name': document['handler_profile_name'],
        'queue_time': document['queue_time'].isoformat(),
        'timeout_seconds': document[
            'timeout_seconds'] if 'timeout_seconds' in document else 7200,
        'callback_url': document['callback_url'],
        'relative_path':
            document['relative_path'] if 'relative_path' in document else '',
        'market_resource_id': document[
            'market_resource_id'] if 'market_resource_id' in document else '',
        'market_name':
            document['market_name'] if 'market_name' in document else '',
        'region_name':
            document['region_name'] if 'region_name' in document else ''
    }
