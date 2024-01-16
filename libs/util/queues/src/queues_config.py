from os import path

from dotenv import dotenv_values

env_path = '.env'

if not path.exists(env_path):
    raise Exception('.env request_file not found')

config = dotenv_values(env_path)

REFRESH_QUOTA_SIZE = int(config['REFRESH_QUOTA_SIZE'])
REFRESH_QUEUE_REFILL_TIMEOUT = int(config['REFRESH_QUEUE_REFILL_TIMEOUT'])
