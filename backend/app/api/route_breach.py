from typing import List

from auth.auth_handler import validate_sensitive_search
from core.config import MUST_VERIFY_SEARCH_KEYS
from core.database import get_db
from dependencies.data_leak_dependency import verify_turnstile_token_search
from fastapi import APIRouter, Depends, HTTPException, status
from models.breach import Breach
from models.data_leak import DataLeak
from models.data_type import DataType
from schemas.data_leak import DataLeakInput, DataLeakShow
from sqlalchemy import desc, false
from sqlalchemy.orm import Session
from utils.crytpography import get_hash

router = APIRouter()


@router.post(
    "/data/",
    response_model=List[DataLeakShow],
    dependencies=[Depends(verify_turnstile_token_search)],
)
def get_breaches_info(
    payload: DataLeakInput,
    is_full_search: bool = Depends(validate_sensitive_search),
    db: Session = Depends(get_db),
):
    """Returns information about data breaches related to a value and type

    If searched value and data type matches the information of a valid JWT token, then it includes
    sensitive breaches in its result.
    """
    if payload.dtype in MUST_VERIFY_SEARCH_KEYS and not is_full_search:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Verification is required to search by {payload.dtype}",
        )
    hash_value = get_hash(payload.value)
    dtype = db.query(DataType).filter(DataType.name == payload.dtype).first()
    if dtype is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data type {payload.dtype}",
        )
    breaches_query = (
        db.query(DataLeak)
        .join(Breach, Breach.id == DataLeak.breach_id)
        .filter(DataLeak.hash_value == hash_value)
        .filter(DataLeak.data_type_id == dtype.id)
    )
    if not is_full_search:
        breaches_query = breaches_query.filter(Breach.is_sensitive == false())

    found_breaches = breaches_query.order_by(desc(Breach.breach_date)).all()
    return found_breaches
