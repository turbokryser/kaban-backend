import pytest
from fastapi import status
from app.models import Team
from app.auth import create_access_token


def test_create_team(client, test_user, db):
    """Тест создания команды"""
    token = create_access_token(data={"sub": test_user.id})
    
    response = client.post(
        "/teams",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Test Team"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test Team"
    assert data["owner_id"] == test_user.id
    
    # Проверяем, что команда создана в БД
    team = db.query(Team).filter(Team.id == data["id"]).first()
    assert team is not None
    assert team.name == "Test Team"


def test_create_team_no_auth(client):
    """Тест создания команды без авторизации"""
    response = client.post(
        "/teams",
        json={"name": "Test Team"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_teams(client, test_user, db):
    """Тест получения списка команд"""
    token = create_access_token(data={"sub": test_user.id})
    
    # Создаем команду
    team = Team(name="My Team", owner_id=test_user.id)
    db.add(team)
    db.commit()
    
    # Получаем список команд
    response = client.get(
        "/teams",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(team["name"] == "My Team" for team in data)


def test_list_teams_empty(client, test_user):
    """Тест получения пустого списка команд"""
    token = create_access_token(data={"sub": test_user.id})
    
    response = client.get(
        "/teams",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


