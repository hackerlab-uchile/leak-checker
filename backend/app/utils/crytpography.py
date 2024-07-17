import hmac
from hashlib import sha256

from core.config import HMAC_KEY


def get_hash(value: str) -> str:
    """Calculates the hash of a string value using a secret key

    Args:
        value (str): value to be hashed

    Raises:
        Exception: raises exception if HMAC_KEY is not found

    Returns:
        str: hash of value
    """
    if HMAC_KEY is None:
        raise Exception("HMAC_KEY not found!") from ValueError
    byte_key = HMAC_KEY.encode()
    byte_value = value.encode()
    h = hmac.new(byte_key, byte_value, sha256).hexdigest()
    return h
