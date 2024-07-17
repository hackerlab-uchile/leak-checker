import pytest
from core.database import Base, get_db, get_test_db, test_engine
from dependencies.data_leak_dependency import verify_turnstile_token_search
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from main import app
from models.breach import Breach
from models.data_leak import DataLeak
from models.data_type import DataType
from schemas.data_leak import DataLeakInput
from sqlalchemy.orm import Session
from utils.crytpography import get_hash

TOKEN_ALWAYS_PASSES = "1x0000000000000000000000000000000AA"
TOKEN_ALWAYS_FAILS = "2x0000000000000000000000000000000AA"
TOKEN_ALREADY_SPENT = "3x0000000000000000000000000000000AA"


def override_verify_turnstile_token_search(payload: DataLeakInput):
    if (
        payload.turnstile_response == TOKEN_ALWAYS_FAILS
        or payload.turnstile_response == TOKEN_ALREADY_SPENT
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Turnstile token required",
        )


@pytest.fixture(scope="function")
def db_session():
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = Session(bind=test_engine)

    yield session_

    session_.rollback()
    session_.close()


@pytest.fixture(scope="function")
def turnstile_passes():
    app.dependency_overrides[verify_turnstile_token_search] = (
        override_verify_turnstile_token_search
    )
    yield
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def override_get_db():
    app.dependency_overrides[get_db] = get_test_db
    yield
    app.dependency_overrides = {}  # Clear out the overrides after the test


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def get_available_dtypes(db_session):
    dtypes = {
        "email": DataType(id=1, name="email", display_name="Correo electrónico"),
        "rut": DataType(id=2, name="rut", display_name="RUT"),
        "phone": DataType(id=3, name="phone", display_name="Número telefónico"),
        "credit_card": DataType(
            id=4, name="credit_card", display_name="Tarjeta de crédito"
        ),
        "address": DataType(id=5, name="address", display_name="Domicilio"),
        "ip_address": DataType(id=6, name="ip_address", display_name="Dirección IP"),
        "name": DataType(id=7, name="name", display_name="Nombre"),
        "password": DataType(id=8, name="password", display_name="Contraseña"),
        "username": DataType(id=9, name="username", display_name="Nombre de usuario"),
    }
    db_session.add_all(dtypes.values())
    db_session.commit()
    return dtypes


def create_available_dtypes():
    session = Session(bind=test_engine)
    dtypes: list[DataType] = [
        DataType(id=1, name="email", display_name="Correo electrónico"),
        DataType(id=2, name="rut", display_name="RUT"),
        DataType(id=3, name="phone", display_name="Número telefónico"),
    ]
    session.add_all(dtypes)
    session.commit()
    session.close()


@pytest.fixture(scope="function", autouse=True)
def create_test_tables():
    Base.metadata.create_all(bind=test_engine)
    # create_available_dtypes()
    yield
    for tbl in reversed(Base.metadata.sorted_tables):
        with test_engine.connect() as conn:
            conn.execute(tbl.delete())
            conn.commit()


def email_not_breached(test_client):
    pass
    # response = test_client.post("/data/", json=)


@pytest.fixture(scope="function")
def create_email_breaches(override_get_db, get_available_dtypes, db_session):
    breaches = [
        Breach(
            name="Breach1",
            description="Some breach 1...",
            breach_date="2021-07-03",
            confirmed=True,
            is_sensitive=False,
            data_breached=[
                get_available_dtypes["username"],
                get_available_dtypes["email"],
                get_available_dtypes["password"],
                get_available_dtypes["ip_address"],
            ],
        ),
        Breach(
            name="Breach2",
            description="Some breach 2...",
            breach_date="2023-11-03",
            confirmed=True,
            is_sensitive=False,
            data_breached=[
                get_available_dtypes["email"],
                get_available_dtypes["password"],
            ],
        ),
        Breach(
            name="Breach3",
            description="Some breach 3...",
            breach_date="2020-04-11",
            confirmed=True,
            is_sensitive=False,
            data_breached=[
                get_available_dtypes["username"],
                get_available_dtypes["email"],
                get_available_dtypes["password"],
                get_available_dtypes["credit_card"],
            ],
        ),
    ]
    db_session.add_all(breaches)
    db_session.commit()
    return breaches


@pytest.fixture
def breached_email(create_email_breaches, get_available_dtypes, db_session):
    value = "example@mail.com"
    hvalue = get_hash(value)
    print(f"{create_email_breaches=}")
    dls = [
        DataLeak(
            hash_value=hvalue,
            data_type=get_available_dtypes["email"],
            breach_id=create_email_breaches[0].id,
            found_with=[
                get_available_dtypes["username"],
                get_available_dtypes["email"],
                get_available_dtypes["password"],
                get_available_dtypes["ip_address"],
            ],
        ),
        DataLeak(
            hash_value=hvalue,
            data_type=get_available_dtypes["email"],
            breach_id=create_email_breaches[1].id,
            found_with=[
                get_available_dtypes["email"],
                get_available_dtypes["password"],
            ],
        ),
        DataLeak(
            hash_value=hvalue,
            data_type=get_available_dtypes["email"],
            breach_id=create_email_breaches[2].id,
            found_with=[
                get_available_dtypes["email"],
                get_available_dtypes["credit_card"],
            ],
        ),
    ]
    db_session.add_all(dls)
    db_session.commit()
    return value


def test_get_breachdata_by_email_no_leak(
    test_client, override_get_db, get_available_dtypes, turnstile_passes
):
    """Successful GET /breach/data/ with an email not leaked"""
    data = DataLeakInput(
        value="example@mail.com", dtype="email", turnstile_response=TOKEN_ALWAYS_PASSES
    )
    response = test_client.post("/breach/data/", content=data.model_dump_json())
    assert response.status_code == 200
    assert response.json() == []


def test_get_breachdata_by_email_leak(
    test_client, breached_email, override_get_db, turnstile_passes, db_session
):
    """Successful GET /breach/data/ with a breached email"""
    result = db_session.query(DataLeak).all()
    data = DataLeakInput(
        value=breached_email, dtype="email", turnstile_response=TOKEN_ALWAYS_PASSES
    )
    response = test_client.post("/breach/data/", content=data.model_dump_json())
    assert response.status_code == 200
    assert len(response.json()) == 3
