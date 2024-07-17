from datetime import datetime

from pydantic import BaseModel, PositiveInt


class BreachDataBase(BaseModel):
    breach_id: PositiveInt
    data_type_id: PositiveInt


class BreachDataCreate(BreachDataBase):
    pass


class BreachData(BreachDataBase):
    created_at: datetime
