import secrets
from datetime import timedelta

from core.config import CODE_EXPIRE_MINUTES, CODE_LENGTH, MAX_CODE_TRIES
from models.user import User
from models.verification_code import VerificationCode
from pydantic import PositiveInt
from repositories.data_type_repository import get_data_type_by_name
from schemas.verification_code import (
    VerificationCodeCreate,
    VerificationCodeInput,
)
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false


def generate_random_code() -> str:
    """Returns a random 6-digit sequence of numbers"""
    n = CODE_LENGTH
    output = ""
    for _ in range(n):
        output += str(secrets.choice(range(0, 10)))
    return output


def get_total_codes_created_by_ip_address_under_minutes(
    ip_address: str, minutes: int, db: Session
) -> int:
    """Returns the total number of codes created by the same IP address under the last x minutes"""
    total_codes_created = (
        db.query(VerificationCode)
        .filter(
            VerificationCode.address == ip_address,
            VerificationCode.created_at + timedelta(minutes=minutes) > func.now(),
        )
        .count()
    )
    return total_codes_created


def generate_new_verification_code(
    user_id: PositiveInt, address: str, db: Session
) -> VerificationCode:
    random_code: str = generate_random_code()
    new_code = VerificationCodeCreate(
        code=random_code, user_id=user_id, address=address
    )
    return save_verification_code(db=db, vcode=new_code)


def get_valid_verification_code_if_correct(
    vcode: VerificationCodeInput, db: Session
) -> VerificationCode | None:
    """Returns a valid verification code if matches with the one passed as parameter.
    Otherwise, returns None if the verification code is not valid"""
    input_code = vcode.code
    value = vcode.value
    data_type_name = vcode.dtype
    data_type = get_data_type_by_name(name=data_type_name, db=db)
    if data_type is None:
        return None
    candidate = (
        db.query(VerificationCode)
        .join(User)
        .filter(User.value == value, User.data_type_id == data_type.id)
        .filter(
            VerificationCode.created_at + timedelta(minutes=CODE_EXPIRE_MINUTES)
            > func.now()
        )
        .order_by(desc(VerificationCode.created_at))
        .first()
    )
    if candidate and candidate.tries < MAX_CODE_TRIES:
        candidate.tries += 1
        print(f"{candidate.tries=}")
        db.commit()
        db.refresh(candidate)
    if (
        candidate
        and not candidate.used
        and candidate.tries <= MAX_CODE_TRIES
        and candidate.code == input_code
    ):
        return candidate
    return None


def get_verification_code(
    vcode: VerificationCodeInput, db: Session
) -> VerificationCode | None:
    code = vcode.code
    associated_value = vcode.value
    result = (
        db.query(VerificationCode)
        .join(User, User.id == VerificationCode.user_id)
        .filter(
            VerificationCode.code == code,
            VerificationCode.used == false(),
            User.value == associated_value,
        )
        .first()
    )
    if result:
        return result
    return None


def save_verification_code(
    db: Session, vcode: VerificationCodeCreate
) -> VerificationCode:
    db_item = VerificationCode(**vcode.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_verification_code(db: Session, vcode: VerificationCode) -> None:
    db_item = vcode
    db.delete(db_item)
    db.commit()


def mark_verification_code_as_used(vcode: VerificationCode, db: Session) -> None:
    vcode.used = True
    db.commit()
    db.refresh(vcode)
