from os import path

from dotenv import dotenv_values

env_path = ".env"

if not path.exists(env_path):
    raise Exception(".env file not found")

config = dotenv_values(env_path)

SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = config["ALGORITHM"]

ACCESS_TOKEN_EXPIRE_IN_MINUTES = int(config['ACCESS_TOKEN_EXPIRE_IN_MINUTES'])
