import pytest
from fastapi import status


def test_get_current_user_success(client, test_user):
    """Тест получения информации о текущем пользователе"""
    from app.auth import create_access_token
    
    # Создаем токен
    token = create_access_token(data={"sub": test_user.id})
    
    # Получаем информацию о пользователе
    response = client.get(
        "/user/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user.email
    assert data["username"] == test_user.username
    assert data["id"] == test_user.id


def test_get_current_user_no_token(client):
    """Тест получения информации без токена"""
    response = client.get("/user/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_invalid_token(client):
    """Тест получения информации с невалидным токеном"""
    response = client.get(
        "/user/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_inactive(client, inactive_user):
    """Тест получения информации с неактивным аккаунтом"""
    from app.auth import create_access_token
    
    token = create_access_token(data={"sub": inactive_user.id})
    
    response = client.get(
        "/user/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


