from .enums import Environment


def is_internal_environment(environment: Environment):
    return environment in [
        Environment.LOCAL,
        Environment.DEVELOPMENT,
        Environment.TESTING,
    ]
