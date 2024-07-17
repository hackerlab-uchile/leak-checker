from core.database import Base, engine, test_engine
from models.breach import Breach
from models.breach_data import BreachData
from models.data_found_with import DataFoundWith
from models.data_leak import DataLeak
from models.data_type import DataType
from models.password import Password
from models.security_tip import SecurityTip
from models.verification_code import VerificationCode
from sqlalchemy_utils import create_database, database_exists

if not database_exists(engine.url):
    create_database(engine.url)
Base.metadata.create_all(bind=engine)

if not database_exists(test_engine.url):
    create_database(test_engine.url)
Base.metadata.create_all(bind=test_engine)
