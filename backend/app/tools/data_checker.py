import re
from enum import Enum
from typing import Callable


class DataType(Enum):
    EMAIL = "email"
    PHONE = "phone"
    RUT = "rut"
    HASH = "hash"
    IP_ADDR = "ip_address"
    CREDIT_CARD = "credit_card"
    DATE = "date"
    STRING = "string"
    NUMERIC = "numeric"


class DataChecker:
    def __init__(
        self,
        dtype: DataType,
        regex_list: list[str],
        sanitize_func: Callable[[str], str] = lambda x: x,
    ):
        self.dtype = dtype
        self._compile_regex(regex_list)
        self.sanitize_func = sanitize_func

    def _compile_regex(self, regex_list: list[str]) -> None:
        raw_regex = r"|".join(regex_list)
        self.regex = re.compile(raw_regex)

    def match(self, value: str) -> bool:
        san_value = self.sanitize_func(value)
        return True if self.regex.match(san_value) else False
