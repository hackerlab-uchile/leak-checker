from datetime import timedelta

from pydantic import BaseModel


class TokenPayload(BaseModel):
    value: str
    dtype: str


class TokenCreate(TokenPayload):
    expires_delta: timedelta
