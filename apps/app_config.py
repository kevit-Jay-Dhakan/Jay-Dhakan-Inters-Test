from os import path

from dotenv import dotenv_values
from libs.utils.common.src.modules.environments import Environment

env_path = '.env'

if not path.exists(env_path):
    raise Exception('.env request_file not found')

config = dotenv_values(env_path)

ENVIRONMENT = Environment(config['ENVIRONMENT'])
HOST = config.get('HOST', '127.0.0.1')
PORT = int(config.get('PORT', 3000))
