from typing import Any


class FieldConfig:
    def __init__(
        self,
        minimum: int = None,
        maximum: int = None,
        min_length: int = None,
        max_length: int = None,
        default: Any = None
    ):
        if minimum is not None:
            self.minimum = minimum

        if maximum is not None:
            self.maximum = maximum

        if min_length is not None:
            self.min_length = min_length

        if max_length is not None:
            self.max_length = max_length

        if default is not None:
            self.default = default
