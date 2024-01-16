from libs.util.db.mongoose.src import BaseRepository
from libs.util.queues.src.collection_queue import CollectionQueue


class HandlerQueue(CollectionQueue):
    def __init__(self, repository: BaseRepository = None):
        handler_list = [
            filter_handler_fields(doc)
            for doc in repository.find({'pause': False})
        ]
        super().__init__(document_list=handler_list)

    def enqueue(
        self, item, force: bool = False,
        is_got_modified_handler_name_in_collect: bool = False
    ):
        with (self.lock):
            index = None
            for i, e_item in enumerate(list(self.document)):
                if (
                    e_item['handler_profile_name'] ==
                    item['handler_profile_name']
                ):
                    index = i
                    break

            if index is None:
                if is_got_modified_handler_name_in_collect:
                    for i, e_item in enumerate(list(self.document)):
                        modified_handler_name = e_item.get(
                            'modified_handler_name', None
                        )
                        if (
                            modified_handler_name and modified_handler_name ==
                            item['handler_profile_name']
                        ):
                            self.document[i]['handler_profile_name'] = \
                                item['handler_profile_name']
                            self.document[i]['url'] = item['url']
                            del self.document[i]['error']
                            del self.document[i]['modified_handler_name']
                            return None

                self.document.append(item)
                return None
            elif force is True:
                self.document[index] = item
                return None
            else:
                return None

    def add_handler(
        self, item, force: bool = False,
        is_got_modified_handler_name_in_collect: bool = False
    ):
        return self.enqueue(
            item, force, is_got_modified_handler_name_in_collect
        )

    def get_handler(self):
        return self.dequeue()

    def get_length(self):
        with self.lock:
            return len(list(self.document))

    def get_list(self):
        with self.lock:
            return list(self.document)


def filter_handler_fields(document):
    filter_doc = {
        'url': str(document['url']),
        'count': int(document['count']),
        'handler_profile_name': document['handler_profile_name']
    }
    if 'handler_id' in document:
        filter_doc['handler_id'] = document['handler_id']

    if 'modified_handler_name' in document:
        filter_doc['modified_handler_name'] = document['modified_handler_name']

    if 'error' in document:
        filter_doc['error'] = document['error']
    return filter_doc
