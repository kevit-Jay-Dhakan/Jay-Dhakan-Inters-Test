import threading
from collections import deque

from libs.util.logger.src import log_helper


class CollectionQueue:
    def __init__(self, document_list: list[dict] = None):
        if document_list is None:
            document_list = []
        self.lock = threading.Lock()  # only one thread can use this at a time
        self.document = deque(document_list)

    def enqueue(self, item):
        with self.lock:
            return self.document.append(item)

    def dequeue(self):
        with self.lock:
            try:
                return self.document.popleft()
            except IndexError:
                return None

    def remove_item(self, request_data):
        with self.lock:
            try:
                return self.document.remove(request_data)
            except ValueError:
                log_helper.critical(f'QUEUE - {request_data}', exc_info=True)
                return None

    def update_item(self, request_data):
        with self.lock:
            for i, e_item in enumerate(list(self.document)):
                if (
                    e_item['slave_request_time'] ==
                    request_data.slave_request_time
                ):
                    self.document[i] = request_data
                    break

    def remove_handler(self, handler_profile_name: str):
        with self.lock:
            for i, item in enumerate(list(self.document)):
                if item['handler_profile_name'] == handler_profile_name:
                    self.document.remove(item)
