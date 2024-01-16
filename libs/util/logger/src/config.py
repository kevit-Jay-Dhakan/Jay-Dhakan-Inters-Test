from os import path

from dotenv import dotenv_values

env_path = '.env'

if not path.exists(env_path):
    raise Exception('.env request_file not found')

config = dotenv_values(env_path)

LOGGER_ENABLED = config.get('LOGGER_ENABLED', True)

SHOW_CRITICAL_LOGS = config.get('SHOW_CRITICAL_LOGS', True)
SHOW_DEBUG_LOGS = config.get('SHOW_DEBUG_LOGS', True)
SHOW_ERROR_LOGS = config.get('SHOW_ERROR_LOGS', True)
SHOW_INFO_LOGS = config.get('SHOW_INFO_LOGS', True)
SHOW_WARN_LOGS = config.get('SHOW_WARN_LOGS', True)
