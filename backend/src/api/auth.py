from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import timedelta
from ..models import UserCreate, UserRead
from ..services.user_service import UserService
from ..services.auth_service import AuthUtils
from ..database.database import get_session
from ..services.auth_service import ACCESS_TOKEN_EXPIRE_MINUTES, Token


router = APIRouter()


@router.post("/register", response_model=UserRead)
def register_user(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user.
    """
    try:
        user = UserService.create_user(session, user_create)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
def login_user(user_credentials: UserCreate, session: Session = Depends(get_session)):
    """
    Authenticate a user and return an access token.
    """
    user = AuthUtils.authenticate_user(
        session, user_credentials.email, user_credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthUtils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
def logout_user():
    """
    Logout the current user.
    """
    # In a real implementation, you might add the token to a blacklist
    return {"message": "Successfully logged out"}