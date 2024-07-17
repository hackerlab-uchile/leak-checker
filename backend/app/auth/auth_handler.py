from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from core.config import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyCookie
from schemas.data_leak import DataLeakInput
from schemas.token import TokenPayload
from schemas.user import UserInfo

cookie_scheme = APIKeyCookie(
    name="token", description="Allows sensitive breaches search", auto_error=False
)


def create_jwt_token(
    value: str,
    dtype: str,
    expires_delta: timedelta = timedelta(minutes=JWT_EXPIRE_MINUTES),
) -> str:
    payload = {
        "value": value,
        "dtype": dtype,
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def get_jwt_token(token: Optional[str] = Security(cookie_scheme)) -> TokenPayload:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    if token is None:
        print("NO TOKEN")
        raise credentials_exception
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        value = payload.get("value")
        dtype = payload.get("dtype")
        if value is None or dtype is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    return TokenPayload(value=value, dtype=dtype)


def get_current_active_user(
    token: Optional[str] = Security(cookie_scheme),
) -> UserInfo | None:
    if token is None:
        return None
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        value = payload.get("value")
        dtype = payload.get("dtype")
        exp = payload.get("exp")
        if value is None or dtype is None or exp is None:
            return None
    except jwt.InvalidTokenError:
        return None
    return UserInfo(value=value, dtype=dtype, exp=exp)


def validate_sensitive_search(
    payload: DataLeakInput, token: Optional[str] = Security(cookie_scheme)
) -> bool:
    try:
        response = False
        token_decode = get_jwt_token(token=token)
        if payload.dtype == token_decode.dtype and payload.value == token_decode.value:
            response = True
    except HTTPException as e:
        return False
    return response
