from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..models.user import UserRead
from ..database.database import get_session
from ..api.deps import get_current_user
from ..models.user import User


router = APIRouter()


@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get the current user's information.
    """
    return UserRead(
        id=current_user.id,
        email=current_user.email,
        createdAt=current_user.createdAt,
        updatedAt=current_user.updatedAt
    )