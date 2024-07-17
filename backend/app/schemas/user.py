from datetime import datetime

from pydantic import BaseModel, PositiveInt


class UserBase(BaseModel):
    value: str


class UserCreate(UserBase):
    data_type_id: PositiveInt


class UserInfo(UserBase):
    dtype: str
    exp: datetime
