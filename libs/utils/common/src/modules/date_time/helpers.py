from datetime import datetime
from typing import List

import pytz


def convert_date_to_timezones(
    date: datetime,
    timezones: List[str] = None
) -> dict:
    if not isinstance(date, datetime):
        raise ValueError('Input must be a datetime object.')

    if timezones is None:
        timezones = ['UTC', 'Asia/Kolkata']

    result = {}

    _date = date.now()
    for tz_str in timezones:
        try:
            tz = pytz.timezone(tz_str)
            result[tz_str] = _date.astimezone(tz).isoformat()
        except pytz.UnknownTimeZoneError:
            result[tz_str] = 'Invalid time zone'

    return result
