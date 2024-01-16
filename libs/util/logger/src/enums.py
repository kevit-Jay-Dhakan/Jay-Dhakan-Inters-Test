from enum import Enum


class LogLevel(Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    ERROR = 'ERROR'
    WARN = 'WARN'
    CRITICAL = 'CRITICAL'


class LogColor(Enum):
    DEBUG = '0394fc'
    INFO = '0066ff'
    ERROR = 'ff6600'
    WARN = 'd9cb09'
    CRITICAL = 'ff0000'
