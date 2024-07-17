from typing import List

from pydantic import BaseModel, PositiveInt


class DataTypeBase(BaseModel):
    name: str


class DataTypeCreate(DataTypeBase):
    pass


class DataType(DataTypeBase):
    id: PositiveInt


class DataTypeShow(DataTypeBase):
    security_tips: List[str]
