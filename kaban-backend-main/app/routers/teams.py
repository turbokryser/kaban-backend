from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Team
from app.schemas import TeamCreate, TeamResponse
from app.auth import get_current_user

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    team_data: TeamCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    team = Team(
        name=team_data.name,
        owner_id=current_user.id
    )
    db.add(team)
    db.commit()
    db.refresh(team)

    return team


@router.get("", response_model=List[TeamResponse])
async def list_teams(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get teams where user is owner or member
    teams = db.query(Team).filter(Team.owner_id == current_user.id).all()
    return teams




