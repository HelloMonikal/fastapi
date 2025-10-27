from fastapi.testclient import TestClient
import pytest
from app.main import app
from sqlalchemy import create_engine
from app.database import Base
from app.database import get_db
from sqlalchemy.orm import sessionmaker
from app.config import settings


SQLALCHEMY_DATABASE_URL  = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TesstingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


# put override_get_db in fixture 
# def override_get_db():
#     db = TesstingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# kind of need to walk though these codes
@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TesstingSessionLocal()
    try:
        yield db
    finally: 
        db.close()


# set dependency on session
@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally: 
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

