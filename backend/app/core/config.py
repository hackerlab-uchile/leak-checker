import os
import warnings


class EnvironmentVariableWarning(UserWarning):
    pass


def get_env_value(key, default="") -> str:
    try:
        value = os.environ[key].strip()
    except KeyError:
        warnings.warn(
            f"Env variable {key} doesn't exist. Using default value: '{default}'",
            EnvironmentVariableWarning,
        )
        return default
    return value


def get_int_from_env(key, default: int = 0) -> int:
    try:
        value = int(os.environ.get(key, default=default))
    except ValueError:
        warnings.warn(
            f"Tried accessing int variable {key}, but had an invalid int value. Using default value: '{default}'",
            EnvironmentVariableWarning,
        )
        return default
    return value


def get_bool_from_env(key, default: bool = False) -> bool:
    value = os.environ.get(key, default=None)
    if value is not None and value.lower() == "true":
        return True
    elif value is not None and value.lower() == "false":
        return False
    return default


# General purpopse
IN_PROD: bool = get_bool_from_env("IN_PROD", False)
HMAC_KEY: str = get_env_value("HMAC_KEY")
BACKEND_URL: str = get_env_value("BACKEND_URL", "http://localhost:8000")
POPULATE_DUMMY_DATA: bool = get_bool_from_env("POPULATE_DUMMY_DATA", False)

# Database connection
POSTGRES_USER: str = get_env_value("PGUSER")
POSTGRES_PASSWORD: str = get_env_value("POSTGRES_PASSWORD")
POSTGRES_SERVER: str = get_env_value("POSTGRES_SERVER")
POSTGRES_DB: str = get_env_value("POSTGRES_DB")
POSTGRES_TEST_DB: str = get_env_value("POSTGRES_TEST_DB")

# SMTP / Email sender
SMTP_USERNAME: str = get_env_value("SMTP_USERNAME")
SMTP_PASSWORD: str = get_env_value("SMTP_PASSWORD")
SMTP_SERVER: str = get_env_value("SMTP_SERVER")
SMTP_PORT: int = get_int_from_env("SMTP_PORT", 587)
SMTP_FROM_NAME: str = get_env_value("SMTP_FROM_NAME", "Data-Leak-Checker")

# JWT Config
JWT_SECRET: str = get_env_value("JWT_SECRET")
JWT_ALGORITHM: str = get_env_value("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES: int = get_int_from_env("JWT_EXPIRE_MINUTES", 10)

# Twilio / SMS sender
TWILIO_AUTH_TOKEN: str = get_env_value("TWILIO_AUTH_TOKEN")
TWILIO_ACCOUNT_SID: str = get_env_value("TWILIO_ACCOUNT_SID")
TWILIO_SENDER_NUMBER: str = get_env_value("TWILIO_SENDER_NUMBER")
TWILIO_SENDER_NUMBER: str = get_env_value("TWILIO_SENDER_NUMBER")
DEV_RECEIVER_NUMBER: str = get_env_value("DEV_RECEIVER_NUMBER")

# OAuth Config
CLIENT_ID: str = get_env_value("CLIENT_ID")
CLIENT_SECRET: str = get_env_value("CLIENT_SECRET")

# Verification Code
CODE_LENGTH: int = get_int_from_env("CODE_LENGTH", 8)
CODE_EXPIRE_MINUTES: int = get_int_from_env("CODE_EXPIRE_MINUTES", 5)
MAX_CODE_TRIES: int = get_int_from_env("MAX_CODE_TRIES", 3)
MAX_CODES_CREATED: int = get_int_from_env("MAX_CODES_CREATED", 5)
CODE_MINUTES_RANGE_LIMIT: int = get_int_from_env("CODE_MINUTES_RANGE_LIMIT", 30)

# Enabled Search Keys
ENABLED_SEARCH_KEYS: list[str] = get_env_value(
    "ENABLED_SEARCH_KEYS", "email,phone,rut"
).split(",")
ENABLED_VERIFICATION_SEARCH_KEYS: list[str] = get_env_value(
    "ENABLED_VERIFICATION_SEARCH_KEYS", "email,phone,rut"
).split(",")
MUST_VERIFY_SEARCH_KEYS: list[str] = get_env_value(
    "MUST_VERIFY_SEARCH_KEYS", "email"
).split(",")

# Frontend
FRONTEND_URL: str = get_env_value("FRONTEND_URL", "http://localhost:3000")

# Cloudflare
CLOUDFLARE_SECRET_KEY: str = get_env_value("CLOUDFLARE_SECRET_KEY")
CLOUDFLARE_ENABLED: bool = get_bool_from_env("CLOUDFLARE_ENABLED", True)
