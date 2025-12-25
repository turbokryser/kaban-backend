import pytest
from fastapi import status
from app.models import User
from app.auth import create_access_token


def test_register_success(client, db):
    """Тест успешной регистрации"""
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "message" in data
    assert "email" in data
    assert data["email"] == "newuser@example.com"
    
    # Проверяем, что пользователь создан в БД
    user = db.query(User).filter(User.email == "newuser@example.com").first()
    assert user is not None
    assert user.username == "newuser"
    assert user.is_active == False  # Аккаунт должен быть неактивным


def test_register_duplicate_email(client, test_user):
    """Тест регистрации с уже существующим email"""
    response = client.post(
        "/auth/register",
        json={
            "username": "anotheruser",
            "email": "test@example.com",  # Используем email существующего пользователя
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registered" in response.json()["detail"].lower()


def test_login_success(client, test_user):
    """Тест успешного входа"""
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    """Тест входа с неправильным паролем"""
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_inactive_account(client, inactive_user):
    """Тест входа с неактивным аккаунтом"""
    response = client.post(
        "/auth/login",
        json={
            "email": "inactive@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "not activated" in response.json()["detail"].lower()


def test_login_nonexistent_user(client):
    """Тест входа с несуществующим пользователем"""
    response = client.post(
        "/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_token(client, test_user):
    """Тест обновления токена"""
    # Сначала получаем refresh токен через login
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    refresh_token = login_response.json()["refresh_token"]
    
    # Обновляем токен
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_refresh_token_invalid(client):
    """Тест обновления токена с невалидным refresh токеном"""
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "invalid_token"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_activate_account(client, db, inactive_user):
    """Тест активации аккаунта"""
    from app.auth import create_activation_token
    
    # Создаем токен активации
    activation_token = create_activation_token(data={"sub": inactive_user.id})
    
    # Активируем аккаунт
    response = client.get(f"/auth/activate?token={activation_token}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["activated"] == True
    
    # Проверяем, что аккаунт активирован
    user = db.query(User).filter(User.id == inactive_user.id).first()
    assert user.is_active == True


def test_forgot_password(client, test_user):
    """Тест запроса на восстановление пароля"""
    response = client.post(
        "/auth/forgot-password",
        json={"email": "test@example.com"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()


def test_reset_password(client, db, test_user):
    """Тест сброса пароля"""
    from app.auth import create_reset_token, verify_password
    
    # Создаем токен сброса
    reset_token = create_reset_token(data={"sub": test_user.id})
    
    # Сбрасываем пароль
    response = client.post(
        "/auth/reset-password",
        json={
            "token": reset_token,
            "new_password": "newpassword123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    
    # Проверяем, что пароль изменился в БД
    db.refresh(test_user)
    assert verify_password("newpassword123", test_user.password) == True


def test_reset_password_invalid_token(client):
    """Тест сброса пароля с невалидным токеном"""
    response = client.post(
        "/auth/reset-password",
        json={
            "token": "invalid_token",
            "new_password": "newpassword123"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

