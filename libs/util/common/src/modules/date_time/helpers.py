from datetime import datetime, timezone
from math import ceil
from typing import List

import pytz
from pydantic.v1.datetime_parse import parse_duration


# function is only used in report.py request_file
def get_datetime_in_ist(utc_time: datetime = datetime.now(timezone.utc)):
    return utc_time


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


# check this calculation whether to keep this only or not
def get_estimation_time_to_download_video(iso_time: str) -> int:
    duration = parse_duration(iso_time)
    seconds = duration.total_seconds()

    if seconds / 3600 >= 7.5 or seconds < 0:
        return 8  # returns in hour right? 8 hour

    default = 3600  # 1hr
    seconds -= 1800  # subtracted 30min from seconds
    numerator, remainder = divmod(seconds, 1800)
    default += (1800 * numerator)  # added numerator * 30min
    default += 3600 if numerator == 0 else 1800  # added one time more
    timeout_hr = ceil(default / 3600)
    return timeout_hr * 3600  # and here returns in seconds


if __name__ == '__main__':
    pass
