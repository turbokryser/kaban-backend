from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models import PriorityEnum


# Auth Schemas
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    avatar_url: Optional[str] = ""


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Team Schemas
class TeamCreate(BaseModel):
    name: str


class TeamResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Project Schemas
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    team_id: int


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    team_id: int
    desk_id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectInvite(BaseModel):
    email: EmailStr


# Section Schemas
class SectionCreate(BaseModel):
    name: str
    order: int


class SectionUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None


class SectionResponse(BaseModel):
    id: int
    desk_id: int
    name: str
    order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Ticket Schemas
class TicketCreate(BaseModel):
    name: str
    task: str
    priority: PriorityEnum = PriorityEnum.medium
    complexity: int = 1
    section_id: int


class TicketUpdate(BaseModel):
    name: Optional[str] = None
    task: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    complexity: Optional[int] = None
    section_id: Optional[int] = None


class TicketResponse(BaseModel):
    id: int
    name: str
    task: str
    priority: PriorityEnum
    complexity: int
    section_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Board Schemas
class BoardSection(SectionResponse):
    tickets: List[TicketResponse] = []


class BoardResponse(BaseModel):
    desk_id: int
    desk_name: str
    sections: List[BoardSection] = []
