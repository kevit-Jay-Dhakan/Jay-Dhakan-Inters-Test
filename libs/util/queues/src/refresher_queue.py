import threading
import traceback
from datetime import datetime, timedelta, timezone
from queue import Queue

from libs.util.queues.src.queues_config import (
    REFRESH_QUEUE_REFILL_TIMEOUT, REFRESH_QUOTA_SIZE
)
from libs.util.db.mongoose.src import BaseRepository
from libs.util.logger.src import log_helper


class RefreshLock:
    def __init__(self, repository: BaseRepository):
        self.repository = repository
        self.collection_name = self.repository.get_name()
        self.update_query = {'$set': {'refresh_status': 'in_progress'}}
        self.lock = threading.Lock()
        self.queue = Queue()
        self.last_refilled_at = datetime.now() - timedelta(
            minutes=REFRESH_QUEUE_REFILL_TIMEOUT
        )

    @staticmethod
    def refresh_query(
        after_date, before_date, current_time, max_limit
    ) -> dict:
        return {
            'original_refresh_request_time': {
                '$gte': after_date,
                '$lte': before_date
            },
            'next_refresh_time': {'$lt': current_time},
            'last_refresh_request_time': {'$gte': max_limit},
            'refresh_status': 'idle',
            'is_archive': False
        }

    @staticmethod
    def status_query(after_date, before_date, max_limit) -> dict:
        return {
            'original_refresh_request_time': {
                '$gte': after_date,
                '$lte': before_date
            },
            'last_refresh_request_time': {'$gte': max_limit},
            'refresh_status': 'idle',
            'is_archive': False
        }

    def get_item_to_refresh(self):
        current_time = datetime.now(timezone.utc)
        day_before = current_time - timedelta(days=1)
        month_before = current_time - timedelta(days=31)
        year_before = current_time - timedelta(days=366)
        params = [
            (day_before, current_time, current_time,
             current_time - timedelta(hours=3)),  # hourly
            (month_before, day_before, current_time,
             current_time - timedelta(days=3)),  # daily
            (year_before, month_before, current_time,
             current_time - timedelta(days=93))  # monthly
        ]

        with self.lock:
            if (
                self.queue.empty() and
                (datetime.now() - self.last_refilled_at) >
                timedelta(minutes=REFRESH_QUEUE_REFILL_TIMEOUT)
            ):
                try:
                    log_helper.info(
                        f'{self.collection_name} - Refilling refresher queue'
                    )
                    for param in params:
                        items = list(
                            self.repository.find(
                                self.refresh_query(*param)
                            ).limit(REFRESH_QUOTA_SIZE)
                        )
                        self.last_refilled_at = datetime.now()
                        if len(items) != 0:
                            log_helper.info(
                                f'{self.collection_name} - Refresher queue '
                                f'refilled'
                            )
                            [self.queue.put(item) for item in items]
                            break
                except Exception as e:
                    print('Error', e)
                    log_helper.error(f'{e}', send_in_ms_team=True)
                    traceback.print_exc()
                    return None
            if self.queue.empty():
                return None
            item_to_refresh = self.queue.get()
            self.last_refilled_at = datetime.now() - timedelta(
                minutes=REFRESH_QUEUE_REFILL_TIMEOUT
            )
            self.repository.update_one(
                {'_id': item_to_refresh['_id']},
                self.update_query
            )
            return item_to_refresh

    def status_item_to_refresh(self, is_live):
        current_time = datetime.now(timezone.utc)
        day_before = current_time - timedelta(days=1)
        month_before = current_time - timedelta(days=31)
        year_before = current_time - timedelta(days=366)
        if is_live != 'false':
            data = {
                'hourly_items': self.repository.count_documents(
                    self.refresh_query(
                        day_before,
                        current_time,
                        current_time,
                        current_time - timedelta(hours=3)
                    )
                ),
                'daily_items': self.repository.count_documents(
                    self.refresh_query(
                        month_before,
                        day_before,
                        current_time,
                        current_time - timedelta(days=3)
                    )
                ),
                'monthly_items': self.repository.count_documents(
                    self.refresh_query(
                        year_before,
                        month_before,
                        current_time,
                        current_time - timedelta(days=93)
                    )
                )
            }
        else:
            data = {
                'hourly_items': self.repository.count_documents(
                    self.status_query(
                        day_before,
                        current_time,
                        current_time - timedelta(hours=3)
                    )
                ),
                'daily_items': self.repository.count_documents(
                    self.status_query(
                        month_before,
                        day_before,
                        current_time - timedelta(days=3)
                    )
                ),
                'monthly_items': self.repository.count_documents(
                    self.status_query(
                        year_before,
                        month_before,
                        current_time - timedelta(days=93)
                    )
                )
            }
        return data

    def get_length(self):
        return self.queue.qsize()
