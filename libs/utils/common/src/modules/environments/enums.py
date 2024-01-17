from enum import Enum


class Environment(Enum):
    LOCAL = 'local'
    TESTING = 'testing'
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'
