from fastapi import APIRouter, Depends
from app.models import User
from app.schemas import UserResponse
from app.auth import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user




