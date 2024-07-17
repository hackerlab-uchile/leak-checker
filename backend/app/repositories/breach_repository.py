import random

from models.breach import Breach
from models.breach_data import BreachData
from models.data_leak import DataLeak
from models.data_type import DataType
from schemas.breaches import BreachCreate as BreachCreateSchema
from sqlalchemy import false, func, true
from sqlalchemy.orm import Session

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


def create_breach(db: Session, breach: BreachCreateSchema):
    db_item = Breach(**breach.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_random_breaches(
    n_limit: int, dtype: DataType, is_sensitive: bool, db: Session
) -> list[Breach]:
    if n_limit <= 0:
        return []

    breach_query = (
        db.query(Breach).join(BreachData).filter(BreachData.data_type_id == dtype.id)
    )
    if is_sensitive:
        breach_query = breach_query.filter(Breach.is_sensitive == true())
    else:  # public search only
        breach_query = breach_query.filter(Breach.is_sensitive == false())
    rand_breaches = breach_query.order_by(func.random()).limit(n_limit).all()
    rand_breaches.sort(key=lambda x: str(x.breach_date), reverse=True)
    return rand_breaches
