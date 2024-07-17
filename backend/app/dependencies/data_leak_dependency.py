import requests
from core.config import (
    CLOUDFLARE_ENABLED,
    CLOUDFLARE_SECRET_KEY,
)
from fastapi import HTTPException, status
from schemas.data_leak import DataLeakInput


def verify_turnstile_token_search(payload: DataLeakInput):
    if CLOUDFLARE_ENABLED:
        if payload.turnstile_response is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Turnstile token required",
            )
        response = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                "secret": CLOUDFLARE_SECRET_KEY,
                "response": payload.turnstile_response,
            },
        )
        is_valid = response.json().get("success", False)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Turnstile Token",
            )
