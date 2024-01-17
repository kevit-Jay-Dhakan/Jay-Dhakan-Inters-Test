from time import sleep

from pymsteams import connectorcard

from libs.utils.logger.src.logger_config import (
    MS_TEAMS_CRITICAL_LOGS_WEBHOOK_URL, MS_TEAMS_DEBUG_LOGS_WEBHOOK_URL,
    MS_TEAMS_ERROR_LOGS_WEBHOOK_URL, MS_TEAMS_INFO_LOGS_WEBHOOK_URL,
    MS_TEAMS_MESSAGE_RETRY_TIMEOUT_IN_SECONDS, MS_TEAMS_MESSAGE_SEND_RETRIES,
    MS_TEAMS_WARN_LOGS_WEBHOOK_URL, MS_TEAMS_WEBHOOK_ENABLED
)
from libs.utils.logger.src.enums import LogLevel

webhook_url_for_log_level = {
    LogLevel.DEBUG: MS_TEAMS_DEBUG_LOGS_WEBHOOK_URL,
    LogLevel.INFO: MS_TEAMS_INFO_LOGS_WEBHOOK_URL,
    LogLevel.ERROR: MS_TEAMS_ERROR_LOGS_WEBHOOK_URL,
    LogLevel.WARN: MS_TEAMS_WARN_LOGS_WEBHOOK_URL,
    LogLevel.CRITICAL: MS_TEAMS_CRITICAL_LOGS_WEBHOOK_URL
}

color_for_log_level = {
    LogLevel.DEBUG: '0394fc',
    LogLevel.INFO: '75f702',
    LogLevel.ERROR: 'fc8403',
    LogLevel.WARN: 'd9cb09',
    LogLevel.CRITICAL: 'ff0000'
}


def send_message_in_ms_teams(log_level: LogLevel, message: str):
    if not MS_TEAMS_WEBHOOK_ENABLED:
        return

    for _ in range(MS_TEAMS_MESSAGE_SEND_RETRIES):
        try:
            message_obj = connectorcard(webhook_url_for_log_level[log_level])
            message_obj.color(color_for_log_level[log_level])
            message_obj.text(message)
            message_obj.send()
            break
        except Exception as err:
            print(err)
            sleep(MS_TEAMS_MESSAGE_RETRY_TIMEOUT_IN_SECONDS)
