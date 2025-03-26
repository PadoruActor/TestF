import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.config import settings
from app import schemas

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture(scope="session")
def test_db():
    # Используем отдельную тестовую БД
    test_db_url = f"{settings.database_url}_test"
    engine = create_engine(test_db_url)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    # Мокаем TronService
    mock_tron = MagicMock()
    mock_tron.get_address_info.return_value = schemas.AddressInfo(
        address="TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
        bandwidth=1000,
        energy=2000,
        balance=3000
    )

    app.dependency_overrides[get_db] = override_get_db
    app.tron_service = mock_tron

    yield TestClient(app)
    app.dependency_overrides.clear()