from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field, PositiveInt


class BreachBase(BaseModel):
    name: str
    description: str
    breach_date: date
    confirmed: bool
    is_sensitive: bool


class BreachCreate(BreachBase):
    pass


class Breach(BreachBase):
    id: PositiveInt
    created_at: datetime


class BreachShow(BreachBase):
    created_at: datetime
    breached_data: List[str] = Field(validation_alias="display_data_types")
    security_tips: List[str] = Field(validation_alias="security_tips")
