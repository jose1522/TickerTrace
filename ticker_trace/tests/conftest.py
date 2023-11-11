from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from models import get_session, BaseModel

from main import app


# Create an engine with a static connection pool so that the same connection is used for all tests
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseModel.metadata.create_all(engine)


@pytest.fixture(name="session")
def new_session():
    with TestingSessionLocal() as session:
        yield session


@pytest.fixture(name="client")
def get_client():
    def overwrite_session():
        with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = overwrite_session
    client = TestClient(app)
    return client
