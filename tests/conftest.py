from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.core.database import Base
from app.dependencies.dep_database import get_db

engine = create_engine("sqlite:///./test.db")

TestingSessionlocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db():
    session = TestingSessionlocal()
    yield session
    session.close()

def override_get_db():
    db = TestingSessionlocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


