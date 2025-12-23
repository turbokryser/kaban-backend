from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Project, Team, Desk, Section, Ticket, UserToTeam
from app.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectInvite,
    BoardResponse,
    BoardSection,
    TicketResponse
)
from app.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if team exists and user is member or owner
    team = db.query(Team).filter(Team.id == project_data.team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )

    # Check if user is team owner or member
    is_member = (
        team.owner_id == current_user.id or
        db.query(UserToTeam).filter(
            UserToTeam.user_id == current_user.id,
            UserToTeam.team_id == project_data.team_id
        ).first() is not None
    )

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this team"
        )

    # Create desk for the project
    desk = Desk(name=f"{project_data.name} Board", owner_id=current_user.id)
    db.add(desk)
    db.flush()

    # Create default sections
    default_sections = [
        Section(desk_id=desk.id, name="To Do", order=1),
        Section(desk_id=desk.id, name="In Progress", order=2),
        Section(desk_id=desk.id, name="Done", order=3)
    ]
    db.add_all(default_sections)

    # Create project
    project = Project(
        name=project_data.name,
        description=project_data.description,
        team_id=project_data.team_id,
        desk_id=desk.id,
        owner_id=current_user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get projects where user is owner or team member
    projects = db.query(Project).join(Team).join(UserToTeam, Team.id == UserToTeam.team_id).filter(
        (Project.owner_id == current_user.id) |
        (UserToTeam.user_id == current_user.id)
    ).distinct().all()

    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Check if user has access
    team = db.query(Team).filter(Team.id == project.team_id).first()
    is_member = (
        project.owner_id == current_user.id or
        team.owner_id == current_user.id or
        db.query(UserToTeam).filter(
            UserToTeam.user_id == current_user.id,
            UserToTeam.team_id == project.team_id
        ).first() is not None
    )

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project"
        )

    return project


@router.post("/{project_id}/invite", status_code=status.HTTP_200_OK)
async def invite_user(
    project_id: int,
    invite_data: ProjectInvite,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Check if user is project owner
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only project owner can invite users"
        )

    # Find user by email
    user = db.query(User).filter(User.email == invite_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if user is already a team member
    existing_membership = db.query(UserToTeam).filter(
        UserToTeam.user_id == user.id,
        UserToTeam.team_id == project.team_id
    ).first()

    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a team member"
        )

    # Add user to team
    membership = UserToTeam(user_id=user.id, team_id=project.team_id)
    db.add(membership)
    db.commit()

    return {"message": "User invited successfully"}


@router.get("/{project_id}/board", response_model=BoardResponse)
async def get_board(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Check if user has access
    team = db.query(Team).filter(Team.id == project.team_id).first()
    is_member = (
        project.owner_id == current_user.id or
        team.owner_id == current_user.id or
        db.query(UserToTeam).filter(
            UserToTeam.user_id == current_user.id,
            UserToTeam.team_id == project.team_id
        ).first() is not None
    )

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project"
        )

    # Get desk and sections
    desk = db.query(Desk).filter(Desk.id == project.desk_id).first()
    sections = db.query(Section).filter(Section.desk_id == project.desk_id).order_by(Section.order).all()

    # Build board response with tickets
    board_sections = []
    for section in sections:
        tickets = db.query(Ticket).filter(Ticket.section_id == section.id).all()
        section_data = BoardSection(
            id=section.id,
            desk_id=section.desk_id,
            name=section.name,
            order=section.order,
            created_at=section.created_at,
            updated_at=section.updated_at,
            tickets=[TicketResponse(
                id=t.id,
                name=t.name,
                task=t.task,
                priority=t.priority,
                complexity=t.complexity,
                section_id=t.section_id,
                created_at=t.created_at,
                updated_at=t.updated_at
            ) for t in tickets]
        )
        board_sections.append(section_data)

    return BoardResponse(
        desk_id=desk.id,
        desk_name=desk.name,
        sections=board_sections
    )

