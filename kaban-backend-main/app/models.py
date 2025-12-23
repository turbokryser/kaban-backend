from sqlalchemy import Column, BigInteger, String, Text, Integer, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    avatar_url = Column(String(150), default="")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    owned_teams = relationship("Team", back_populates="owner", foreign_keys="Team.owner_id")
    owned_projects = relationship("Project", back_populates="owner", foreign_keys="Project.owner_id")
    owned_desks = relationship("Desk", back_populates="owner", foreign_keys="Desk.owner_id")
    team_memberships = relationship("UserToTeam", back_populates="user")


class Team(Base):
    __tablename__ = "teams"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    owner_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="owned_teams", foreign_keys=[owner_id])
    members = relationship("UserToTeam", back_populates="team")
    projects = relationship("Project", back_populates="team")


class UserToTeam(Base):
    __tablename__ = "UsersToTeams"

    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    team_id = Column(BigInteger, ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="team_memberships")
    team = relationship("Team", back_populates="members")


class Desk(Base):
    __tablename__ = "desk"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    owner_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="owned_desks", foreign_keys=[owner_id])
    sections = relationship("Section", back_populates="desk", order_by="Section.order")
    projects = relationship("Project", back_populates="desk")


class Project(Base):
    __tablename__ = "projects"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    team_id = Column(BigInteger, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    desk_id = Column(BigInteger, ForeignKey("desk.id", ondelete="CASCADE"), nullable=False)
    owner_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    team = relationship("Team", back_populates="projects")
    desk = relationship("Desk", back_populates="projects")
    owner = relationship("User", back_populates="owned_projects", foreign_keys=[owner_id])


class Section(Base):
    __tablename__ = "section"

    id = Column(BigInteger, primary_key=True, index=True)
    desk_id = Column(BigInteger, ForeignKey("desk.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    order = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    desk = relationship("Desk", back_populates="sections")
    tickets = relationship("Ticket", back_populates="section")


class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    task = Column(Text, nullable=False)
    priority = Column(Enum(PriorityEnum), nullable=False, default=PriorityEnum.medium)
    complexity = Column(Integer, nullable=False, default=1)
    section_id = Column(BigInteger, ForeignKey("section.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    section = relationship("Section", back_populates="tickets")




