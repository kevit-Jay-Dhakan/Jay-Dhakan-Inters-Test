import logging
import sys
from logging.handlers import RotatingFileHandler
from os import path
from typing import Optional

from libs.vendors.slack.src import send_message_in_slack
from .config import (
    LOGGER_ENABLED,
    SHOW_CRITICAL_LOGS,
    SHOW_DEBUG_LOGS,
    SHOW_ERROR_LOGS,
    SHOW_INFO_LOGS,
    SHOW_WARN_LOGS
)
from libs.vendors.microsoft.teams.src import (
    send_message_in_ms_teams,
    LogLevel as MSTeamsLogLevel
)
from libs.util.logger.src.enums import LogColor

BASE_DIR = path.dirname(path.dirname(__file__))

# Create a custom log_helper

# Create handlers
c_handler = logging.StreamHandler(sys.stdout)
f_handler = RotatingFileHandler(
    path.join(
        path.join(BASE_DIR, 'logs'),
        'history.log'
    ), maxBytes=10 * 1024 * 1024, backupCount=10, encoding='utf-8'
)
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter(
    f'%(asctime)s - SERVER - %(name)s | 'f'%(levelname)s | %(message)s'
)
f_format = logging.Formatter(
    f'%(asctime)s - SERVER - %(name)s | %(levelname)s | %(message)s'
)

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the log_helper
logger = logging.getLogger('collector')
logger.setLevel(logging.DEBUG)
logger.addHandler(c_handler)
logger.addHandler(f_handler)


class LogHelper:
    @staticmethod
    def debug(
        message: str,
        print_in_console: bool = True,
        send_in_ms_teams: bool = False,
        send_in_slack: bool = False,
        slack_msg: Optional[str] = None
    ):
        if not LOGGER_ENABLED or not SHOW_DEBUG_LOGS:
            return

        if print_in_console:
            logger.debug(message)
        if send_in_ms_teams:
            send_message_in_ms_teams(MSTeamsLogLevel.DEBUG, message)
        if send_in_slack:
            json_data = {
                'attachments': [
                    {
                        'color': f'#{LogColor.DEBUG}',
                        'text': f'{message if slack_msg is None else slack_msg}'
                    }
                ]
            }
            send_message_in_slack(json_data)

    @staticmethod
    def info(
        message: str,
        print_in_console: bool = True,
        send_in_ms_teams: bool = False,
        send_in_slack: bool = False,
        slack_msg: Optional[str] = None
    ):
        # returns if log_helper enable is false or info logs not to be shown
        if not LOGGER_ENABLED or not SHOW_INFO_LOGS:
            return

        if print_in_console:
            logger.info(message)
        if send_in_ms_teams:
            send_message_in_ms_teams(MSTeamsLogLevel.INFO, message)
        if send_in_slack:
            json_data = {
                'attachments': [
                    {
                        'color': f'#{LogColor.INFO}',
                        'text': f'{message if slack_msg is None else slack_msg}'
                    }
                ]
            }
            send_message_in_slack(json_data)

    @staticmethod
    def error(
        message: str,
        exc_info: bool = True,
        print_in_console: bool = True,
        send_in_ms_teams: bool = False,
        send_in_slack: bool = False,
        slack_msg: Optional[str] = None
    ):
        # returns if log_helper enable is false or error logs not to be shown
        if not LOGGER_ENABLED or not SHOW_ERROR_LOGS:
            return

        if print_in_console:
            logger.error(message, exc_info=exc_info)
        if send_in_ms_teams:
            send_message_in_ms_teams(MSTeamsLogLevel.ERROR, message)
        if send_in_slack:
            json_data = {
                'attachments': [
                    {
                        'color': f'#{LogColor.ERROR}',
                        'text': f'{message if slack_msg is None else slack_msg}'
                    }
                ]
            }
            send_message_in_slack(json_data)

    @staticmethod
    def warn(
        message: str,
        exc_info: bool = True,
        print_in_console: bool = True,
        send_in_ms_teams: bool = False,
        send_in_slack: bool = False,
        slack_msg: Optional[str] = None
    ):
        # returns if log_helper enable is false or warn logs not to be shown
        if not LOGGER_ENABLED or not SHOW_WARN_LOGS:
            return

        if print_in_console:
            logger.warning(message, exc_info=exc_info)
        if send_in_ms_teams:
            send_message_in_ms_teams(MSTeamsLogLevel.WARN, message)
        if send_in_slack:
            json_data = {
                'attachments': [
                    {
                        'color': f'#{LogColor.WARN}',
                        'text': f'{message if slack_msg is None else slack_msg}'
                    }
                ]
            }
            send_message_in_slack(json_data)

    @staticmethod
    def critical(
        message: str,
        exc_info: bool = True,
        print_in_console: bool = True,
        send_in_ms_teams: bool = False,
        send_in_slack: bool = False,
        slack_msg: Optional[str] = None
    ):
        # returns if log_helper enable is false or critical logs not to be shown
        if not LOGGER_ENABLED or not SHOW_CRITICAL_LOGS:
            return

        if print_in_console:
            logger.critical(message, exc_info=exc_info)
        if send_in_ms_teams:
            send_message_in_ms_teams(MSTeamsLogLevel.CRITICAL, message)
        if send_in_slack:
            json_data = {
                'attachments': [
                    {
                        'color': f'#{LogColor.CRITICAL}',
                        'text': f'{message if slack_msg is None else slack_msg}'
                    }
                ]
            }
            send_message_in_slack(json_data)


log_helper = LogHelper()
