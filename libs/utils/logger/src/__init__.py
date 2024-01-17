from libs.utils.logger.src.logger_config import (
    LOGGER_ENABLED,
    SHOW_CRITICAL_LOGS,
    SHOW_DEBUG_LOGS,
    SHOW_ERROR_LOGS,
    SHOW_INFO_LOGS,
    SHOW_WARN_LOGS
)
from libs.utils.logger.src.microsoft_teams import send_message_in_ms_teams
from libs.utils.logger.src.enums import LogLevel


class Logger:
    @staticmethod
    def debug(
        message: str,
        print_in_console: bool = True,
        send_in_ms_teams: bool = False
    ):
        if not LOGGER_ENABLED or not SHOW_DEBUG_LOGS:
            return

        if print_in_console:
            print(message)
        if send_in_ms_teams:
            send_message_in_ms_teams(LogLevel.DEBUG, message)

    @staticmethod
    def info(
        message: str,
        print_in_console: bool = True,
        send_in_ms_teams: bool = False
    ):
        if not LOGGER_ENABLED or not SHOW_INFO_LOGS:
            return

        if print_in_console:
            print(message)
        if send_in_ms_teams:
            send_message_in_ms_teams(LogLevel.INFO, message)

    @staticmethod
    def error(
        message: str,
        print_in_console: bool = True,
        send_in_ms_teams: bool = False
    ):
        if not LOGGER_ENABLED or not SHOW_ERROR_LOGS:
            return

        if print_in_console:
            print(message)
        if send_in_ms_teams:
            send_message_in_ms_teams(LogLevel.ERROR, message)

    @staticmethod
    def warn(
        message: str,
        print_in_console: bool = True,
        send_in_ms_teams: bool = False
    ):
        if not LOGGER_ENABLED or not SHOW_WARN_LOGS:
            return

        if print_in_console:
            print(message)
        if send_in_ms_teams:
            send_message_in_ms_teams(LogLevel.WARN, message)

    @staticmethod
    def critical(
        message: str,
        print_in_console: bool = True,
        send_in_ms_teams: bool = False
    ):
        if not LOGGER_ENABLED or not SHOW_CRITICAL_LOGS:
            return

        if print_in_console:
            print(message)
        if send_in_ms_teams:
            send_message_in_ms_teams(LogLevel.CRITICAL, message)


logger = Logger()
