from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional
from ..database.database import get_session
from ..services.auth_service import AuthUtils
from ..models import User


security = HTTPBearer()


def get_db_session(session: Session = Depends(get_session)):
    """
    Get a database session for dependency injection.
    """
    return session


def get_current_user(
    session: Session = Depends(get_db_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get the current user based on the JWT token.
    """
    token = credentials.credentials
    token_data = AuthUtils.verify_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    statement = select(User).where(User.email == token_data.email)
    user = session.exec(statement).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_auth_utils():
    """
    Get authentication utilities for dependency injection.
    """
    return AuthUtils()