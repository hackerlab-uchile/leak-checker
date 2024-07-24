import random
from typing import List

from auth.auth_handler import get_jwt_token, validate_sensitive_search
from core.config import MUST_VERIFY_SEARCH_KEYS
from core.database import get_db
from dependencies.data_leak_dependency import verify_turnstile_token_search
from fastapi import APIRouter, Depends, HTTPException, status
from models.breach import Breach
from models.breach_data import BreachData
from models.data_leak import DataLeak
from models.data_type import DataType
from repositories.breach_repository import get_random_breaches
from schemas.data_leak import DataLeakInput, DataLeakShow
from schemas.token import TokenPayload
from sqlalchemy import true
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

router = APIRouter()


@router.post(
    "/data/",
    response_model=List[DataLeakShow],
    dependencies=[Depends(verify_turnstile_token_search)],
)
def get_breaches_demo(
    payload: DataLeakInput,
    is_full_search: bool = Depends(validate_sensitive_search),
    db: Session = Depends(get_db),
):
    """Returns information about random data breaches (Only for demo purposes)
    If a valid JWT exists and matches the searched value and dtype, then also returns sensitive breaches information
    """
    if payload.dtype in MUST_VERIFY_SEARCH_KEYS and not is_full_search:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Verification is required to search by {payload.dtype}",
        )
    dtype = db.query(DataType).filter(DataType.name == payload.dtype).first()
    if payload.dtype == "email" and not looks_like_email(payload.value):
        return []
    elif payload.dtype == "rut" and not payload.value.isnumeric():
        return []
    elif dtype is None:  # or payload.dtype == "phone":
        # elif dtype is None or payload.dtype == "phone":
        return []

    n_limit = random.randint(2, 5)
    rand_breaches = get_random_breaches(n_limit, dtype, is_sensitive=False, db=db)
    print(f"{is_full_search=}")
    if is_full_search:
        rand_breaches += get_random_breaches(2, dtype, is_sensitive=True, db=db)

    rand_breaches.sort(key=lambda x: str(x.breach_date), reverse=True)
    found_breaches: List[DataLeak] = []
    for breach in rand_breaches:
        dl = DataLeak()
        dl.data_type = dtype
        dl.breach_found = breach
        n_found = len(breach.data_breached)
        roll = random.randint(max(0, n_found - 2), n_found)
        picks = random.sample(breach.data_breached, k=roll)
        found_with = set([dtype, *picks])
        dl.found_with = list(found_with)
        found_breaches.append(dl)

    return found_breaches


@router.post("/data/public/", response_model=List[DataLeakShow])
def get_breaches_public_demo(payload: DataLeakInput, db: Session = Depends(get_db)):
    """Returns information about random data breaches related to a data type.
    Only for demo purposes
    """
    dtype = db.query(DataType).filter(DataType.name == payload.dtype).first()
    if payload.dtype == "email" and not looks_like_email(payload.value):
        return []
    elif payload.dtype == "rut" and not payload.value.isnumeric():
        return []
    elif dtype is None or payload.dtype == "phone":
        return []

    n_limit = random.randint(2, 5)
    rand_breaches = get_random_breaches(n_limit, dtype, is_sensitive=False, db=db)
    rand_breaches.sort(key=lambda x: str(x.breach_date), reverse=True)
    found_breaches: List[DataLeak] = []
    for breach in rand_breaches:
        dl = DataLeak()
        dl.data_type = dtype
        dl.breach_found = breach
        n_found = len(breach.data_breached)
        roll = random.randint(max(0, n_found - 2), n_found)
        picks = random.sample(breach.data_breached, k=roll)
        found_with = set([dtype, *picks])
        dl.found_with = list(found_with)
        found_breaches.append(dl)

    return found_breaches


@router.get("/data/sensitive/", response_model=List[DataLeakShow])
def get_sensitive_breaches_demo(
    payload: TokenPayload = Depends(get_jwt_token), db: Session = Depends(get_db)
):
    """Returns information about random SENSITIVE data breaches related to a data type
    Only for demo purposes
    """
    dtype = db.query(DataType).filter(DataType.name == payload.dtype).first()
    if dtype is None:
        return []
    n_limit = random.randint(2, 5)
    rand_breaches = (
        db.query(Breach)
        .join(BreachData)
        .filter(BreachData.data_type_id == dtype.id, Breach.is_sensitive == true())
        .order_by(func.random())
        .limit(n_limit)
        .all()
    )
    rand_breaches.sort(key=lambda x: str(x.breach_date), reverse=True)
    found_breaches: List[DataLeak] = []
    for breach in rand_breaches:
        dl = DataLeak()
        dl.data_type = dtype
        dl.breach_found = breach
        n_found = len(breach.data_breached)
        roll = random.randint(max(0, n_found - 2), n_found)
        picks = random.sample(breach.data_breached, k=roll)
        found_with = set([dtype, *picks])
        dl.found_with = list(found_with)
        found_breaches.append(dl)
    return found_breaches


def looks_like_email(value: str) -> bool:
    # This is used only for demo purposes
    dot_splitted = value.split(".")
    arroba_splitted = value.split("@")
    result = (
        len(arroba_splitted) == 2
        and len(dot_splitted) > 1
        and len(dot_splitted[-1]) > 1
    )
    return result
