import re

from core.config import ENABLED_SEARCH_KEYS
from fastapi import HTTPException, status
from pydantic import AfterValidator, EmailStr
from typing_extensions import Annotated


def available_search_keys_validator(v: str) -> str:
    """Validates if search identifier is available for search"""
    if v not in ENABLED_SEARCH_KEYS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Available dtype: {[key for key in ENABLED_SEARCH_KEYS]}",
        )
    return v


def chilean_mobile_number_validator(v: str) -> str:
    """Validator for chilean mobile phone numbers"""
    assert isinstance(v, str), "Input must be a string"
    assert len(v) <= 12, f"'{v[:13]}(...)' is more than 12 characters long!"
    pattern = r"\+569[\d]{8}"
    assert (
        re.fullmatch(pattern, v) is not None
    ), f"{v} is not the expected format for a chilean phone number. Example: +56911223344"
    return v


ChileanMobileNumber = Annotated[str, AfterValidator(chilean_mobile_number_validator)]
AvailableSearchKeys = Annotated[str, AfterValidator(available_search_keys_validator)]
EmailStrLowerCase = Annotated[EmailStr, AfterValidator(lambda x: x.lower())]
