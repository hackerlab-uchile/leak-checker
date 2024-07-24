from datetime import datetime, timedelta, timezone

import requests
from auth.auth_handler import create_jwt_token
from authlib.integrations.starlette_client import OAuth, OAuthError
from core.config import (
    BACKEND_URL,
    CLIENT_ID,
    CLIENT_SECRET,
    CODE_LENGTH,
    DEV_RECEIVER_NUMBER,
    FRONTEND_URL,
    IN_PROD,
    JWT_EXPIRE_MINUTES,
    SMTP_FROM_NAME,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_SERVER,
    SMTP_USERNAME,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_SENDER_NUMBER,
)
from core.database import get_db
from dependencies.data_type_dependency import (
    EnabledVerificationSearchKeyChecker,
)
from dependencies.verification_code_dependency import (
    verify_host_rate_limting,
)
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel
from repositories.data_type_repository import get_data_type_by_name
from repositories.user import get_user_or_create
from repositories.verification_code_repository import (
    generate_new_verification_code,
    get_valid_verification_code_if_correct,
    mark_verification_code_as_used,
)
from schemas.custom_fields import ChileanMobileNumber, EmailStrLowerCase
from schemas.verification_code import VerificationCodeInput
from sqlalchemy.orm import Session

router = APIRouter()


oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        "scope": "openid email profile",
        "redirect_url": BACKEND_URL + "/verify/oauth/",
    },
)


class PhoneBody(BaseModel):
    phone: ChileanMobileNumber
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "phone": "+56912345678",
                }
            ]
        }
    }


class EmailBody(BaseModel):
    email: EmailStrLowerCase


def get_mail_conf() -> ConnectionConfig | None:
    if SMTP_PASSWORD and SMTP_USERNAME and SMTP_SERVER:
        return ConnectionConfig(
            MAIL_USERNAME=SMTP_USERNAME,
            MAIL_PASSWORD=SMTP_PASSWORD,
            MAIL_FROM=SMTP_USERNAME,
            MAIL_FROM_NAME=SMTP_FROM_NAME,
            MAIL_PORT=SMTP_PORT,
            MAIL_SERVER=SMTP_SERVER,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )
    print(
        "Warning: Couldn't complete email configuration. USERNAME, PASSWORD or SERVER for SMTP server not found"
    )
    return None


@router.post(
    "/send/email/",
    dependencies=[
        Depends(EnabledVerificationSearchKeyChecker("email")),
        Depends(verify_host_rate_limting),
    ],
)
async def send_email_verify(
    background_task: BackgroundTasks,
    payload: EmailBody,
    request: Request,
    db: Session = Depends(get_db),
):
    if request.client is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    email = payload.email
    email_dtype = get_data_type_by_name(name="email", db=db)
    if email_dtype is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    user = get_user_or_create(value=email, data_type_id=email_dtype.id, db=db)
    vcode = generate_new_verification_code(
        user_id=user.id, address=request.client.host, db=db
    )
    html = f"""<p>¡Hola! A continuación, puedes ver tu código de verificación. ¡No lo compartas!</p>
    <p><b>{vcode.format_code_to_send}</b></p>
    """
    message = MessageSchema(
        subject="Verificación de correo electrónico",
        recipients=[email],
        body=html,
        subtype=MessageType.html,
    )
    conf = get_mail_conf()
    if conf:
        fm = FastMail(conf)
        background_task.add_task(fm.send_message, message)
        return JSONResponse(
            status_code=200,
            content={"message": "email has been sent", "code_length": CODE_LENGTH},
        )
    return JSONResponse(status_code=503, content={"message": "Service unavailable"})


@router.post(
    "/send/sms/",
    dependencies=[
        Depends(EnabledVerificationSearchKeyChecker("phone")),
        Depends(verify_host_rate_limting),
    ],
)
async def send_sms_verify(
    payload: PhoneBody, request: Request, db: Session = Depends(get_db)
):
    if request.client is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    phone = payload.phone
    phone_dtype = get_data_type_by_name(name="phone", db=db)
    if phone_dtype is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    user = get_user_or_create(value=phone, data_type_id=phone_dtype.id, db=db)
    vcode = generate_new_verification_code(
        user_id=user.id, address=request.client.host, db=db
    )
    msg = f"Su código de verificación: {vcode.code}. ¡No lo compartas!"
    url = (
        f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    )
    receiver_number = DEV_RECEIVER_NUMBER
    if IN_PROD:
        receiver_number = phone
    data = {"From": TWILIO_SENDER_NUMBER, "To": receiver_number, "Body": msg}
    auth = (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    response = requests.post(url, data=data, auth=auth)
    if response.status_code == 201:
        return JSONResponse(
            status_code=200,
            content={"message": "Sms has been sent", "code_length": CODE_LENGTH},
        )
    return JSONResponse(status_code=400, content={"message": "Sms was not sent"})


@router.get("/rut/", dependencies=[Depends(EnabledVerificationSearchKeyChecker("rut"))])
async def verify_rut(request: Request):
    redirect_uri = request.url_for("oauth_verification")
    if oauth.google is None:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE)
    print(f"{redirect_uri=}")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get(
    "/oauth/", dependencies=[Depends(EnabledVerificationSearchKeyChecker("rut"))]
)
async def oauth_verification(request: Request):
    if oauth.google is None:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE)
    try:
        oauth_response = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    # TODO si se desea usar Clave Única:
    # 1) Debería tomar la respuesta, generar un JWT con el RUT de respuesta
    # 2) associated_value debería corresponder al RUT entregado por CU
    # 3) Entregar JWT al usuario
    associated_value = "11111111-1"
    token = create_jwt_token(associated_value, "rut")
    response = RedirectResponse(
        FRONTEND_URL + f"/?search={associated_value}&type=rut", status_code=302
    )
    response.set_cookie(
        key="token",
        value=token,
        expires=datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES),
        secure=IN_PROD,  # Use false for development purposes
        httponly=True,
        samesite="strict",
    )
    return response


@router.post("/code/")
async def verify_code(
    verification_code: VerificationCodeInput, db: Session = Depends(get_db)
):
    vcode = get_valid_verification_code_if_correct(verification_code, db)
    if vcode is None:
        return JSONResponse(
            status_code=200,
            content={"message": "Invalid verification code", "valid": False},
        )
    token = create_jwt_token(vcode.associated_value, vcode.value_type)
    mark_verification_code_as_used(vcode=vcode, db=db)
    response = JSONResponse(
        status_code=200,
        content={"message": "Code verification successful", "valid": True},
    )
    response.set_cookie(
        key="token",
        value=token,
        expires=datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES),
        secure=IN_PROD,  # Use false for development purposes
        httponly=True,
        samesite="strict",
    )
    return response
