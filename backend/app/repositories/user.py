from core.database import get_db
from fastapi import Depends, HTTPException, status
from models.user import User
from pydantic import PositiveInt
from schemas.user import UserCreate
from sqlalchemy.orm import Session


def get_user_or_create(value: str, data_type_id: PositiveInt, db: Session) -> User:
    existing_user = (
        db.query(User)
        .filter(User.value == value, User.data_type_id == data_type_id)
        .first()
    )
    if existing_user:
        return existing_user
    return create_new_user(UserCreate(value=value, data_type_id=data_type_id), db=db)


def get_user_by_value(value: str, db: Session = Depends(get_db)):
    person = db.query(User).filter(User.value == value).first()
    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="value not found"
        )
    return person


def create_new_user(user: UserCreate, db: Session) -> User:
    db_item = User(**user.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
