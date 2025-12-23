from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Project, Section, Team, UserToTeam
from app.schemas import SectionCreate, SectionUpdate, SectionResponse
from app.auth import get_current_user

router = APIRouter(prefix="/projects/{project_id}/sections", tags=["sections"])


@router.post("", response_model=SectionResponse, status_code=status.HTTP_201_CREATED)
async def create_section(
    project_id: int,
    section_data: SectionCreate,
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

    section = Section(
        desk_id=project.desk_id,
        name=section_data.name,
        order=section_data.order
    )
    db.add(section)
    db.commit()
    db.refresh(section)

    return section


@router.patch("/{section_id}", response_model=SectionResponse)
async def update_section(
    project_id: int,
    section_id: int,
    section_data: SectionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    section = db.query(Section).filter(
        Section.id == section_id,
        Section.desk_id == project.desk_id
    ).first()

    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
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

    # Update section
    if section_data.name is not None:
        section.name = section_data.name
    if section_data.order is not None:
        section.order = section_data.order

    db.commit()
    db.refresh(section)

    return section




