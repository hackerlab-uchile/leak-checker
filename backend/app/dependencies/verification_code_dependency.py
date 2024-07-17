from core.database import get_db
from fastapi import Depends, HTTPException, Request, status
from repositories.verification_code_repository import (
    get_total_codes_created_by_ip_address_under_minutes,
)
from sqlalchemy.orm import Session


def verify_host_rate_limting(request: Request, db: Session = Depends(get_db)):
    max_requests = 5
    minutes_range = 30
    if request.client:
        total_requests = get_total_codes_created_by_ip_address_under_minutes(
            request.client.host, minutes=minutes_range, db=db
        )
        if total_requests >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Try again later",
            )
        return total_requests
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Request must have client host address",
    )
