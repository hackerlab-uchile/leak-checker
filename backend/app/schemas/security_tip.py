from pydantic import BaseModel, PositiveInt


class SecurityTipBase(BaseModel):
    description: str
    data_type_id: PositiveInt


class SecurityTipCreate(SecurityTipBase):
    pass


class SecurityTipShow(SecurityTipBase):
    class Config:
        from_attributes = True
