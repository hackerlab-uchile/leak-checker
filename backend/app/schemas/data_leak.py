from typing import Annotated, List, Optional

from pydantic import AfterValidator, BaseModel, Field, PositiveInt
from schemas.breaches import Breach as BreachSchema
from schemas.breaches import BreachShow
from schemas.custom_fields import AvailableSearchKeys
from schemas.data_types import DataType as DataTypeSchema


class DataLeakInput(BaseModel):
    value: Annotated[str, AfterValidator(lambda x: x.lower())]
    dtype: AvailableSearchKeys
    turnstile_response: Optional[str] = None


class DataLeakBase(BaseModel):
    hash_value: str


class DataLeakCreate(DataLeakBase):
    pass


class DataLeak(DataLeakBase):
    id: PositiveInt
    data_type: DataTypeSchema
    breach_found: BreachSchema
    found_with: List[DataTypeSchema]


class DataLeakShow(BaseModel):
    data_type: str = Field(validation_alias="data_type_display")
    breach: BreachShow = Field(validation_alias="breach_found")
    found_with: List[str] = Field(validation_alias="found_with_display")
    # security_tips: List[str] = Field(validation_alias="breach_security_tips")
