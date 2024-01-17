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

MS_TEAMS_WEBHOOK_ENABLED = config.get('MS_TEAMS_WEBHOOK_ENABLED', True)
MS_TEAMS_DEBUG_LOGS_WEBHOOK_URL = config.get('MS_TEAMS_DEBUG_LOGS_WEBHOOK_URL')
MS_TEAMS_INFO_LOGS_WEBHOOK_URL = config.get('MS_TEAMS_INFO_LOGS_WEBHOOK_URL')
MS_TEAMS_ERROR_LOGS_WEBHOOK_URL = config.get('MS_TEAMS_ERROR_LOGS_WEBHOOK_URL')
MS_TEAMS_WARN_LOGS_WEBHOOK_URL = config.get('MS_TEAMS_WARN_LOGS_WEBHOOK_URL')
MS_TEAMS_CRITICAL_LOGS_WEBHOOK_URL = config.get(
    'MS_TEAMS_CRITICAL_LOGS_WEBHOOK_URL'
)
MS_TEAMS_MESSAGE_SEND_RETRIES = int(
    config.get('MS_TEAMS_MESSAGE_SEND_RETRIES', 3)
)
MS_TEAMS_MESSAGE_RETRY_TIMEOUT_IN_SECONDS = int(
    config.get('MS_TEAMS_MESSAGE_RETRY_TIMEOUT_IN_SECONDS', 5)
)
