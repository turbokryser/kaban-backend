import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models import User
from main import app
from app.auth import get_password_hash


# Тестовая база данных в памяти (SQLite для тестов)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Создает тестовую БД для каждого теста"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Создает тестовый клиент с переопределенной БД"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    # Мокаем отправку email для всех тестов
    with patch('app.routers.auth.send_activation_email', return_value=True), \
         patch('app.routers.auth.send_reset_password_email', return_value=True):
        app.dependency_overrides[get_db] = override_get_db
        with TestClient(app) as test_client:
            yield test_client
        app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    """Создает тестового пользователя"""
    user = User(
        username="testuser",
        email="test@example.com",
        password=get_password_hash("testpassword123"),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def inactive_user(db):
    """Создает неактивного тестового пользователя"""
    user = User(
        username="inactiveuser",
        email="inactive@example.com",
        password=get_password_hash("testpassword123"),
        is_active=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
