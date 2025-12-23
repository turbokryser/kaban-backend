from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Project, Ticket, Section, Team, UserToTeam
from app.schemas import TicketCreate, TicketUpdate, TicketResponse
from app.auth import get_current_user

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])


@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    project_id: int,
    task_data: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Check if section belongs to project's desk
    section = db.query(Section).filter(
        Section.id == task_data.section_id,
        Section.desk_id == project.desk_id
    ).first()

    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found or doesn't belong to this project"
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

    ticket = Ticket(
        name=task_data.name,
        task=task_data.task,
        priority=task_data.priority,
        complexity=task_data.complexity,
        section_id=task_data.section_id
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


@router.patch("/{task_id}", response_model=TicketResponse)
async def update_task(
    project_id: int,
    task_id: int,
    task_data: TicketUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    ticket = db.query(Ticket).join(Section).filter(
        Ticket.id == task_id,
        Section.desk_id == project.desk_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
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

    # If section_id is being updated, verify it belongs to the project
    if task_data.section_id is not None:
        new_section = db.query(Section).filter(
            Section.id == task_data.section_id,
            Section.desk_id == project.desk_id
        ).first()
        if not new_section:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Section doesn't belong to this project"
            )

    # Update ticket
    if task_data.name is not None:
        ticket.name = task_data.name
    if task_data.task is not None:
        ticket.task = task_data.task
    if task_data.priority is not None:
        ticket.priority = task_data.priority
    if task_data.complexity is not None:
        ticket.complexity = task_data.complexity
    if task_data.section_id is not None:
        ticket.section_id = task_data.section_id

    db.commit()
    db.refresh(ticket)

    return ticket




