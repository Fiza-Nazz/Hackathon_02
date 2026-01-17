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
    
    # 1. Try JWT verification first (as per spec)
    token_data = AuthUtils.verify_token(token)
    
    # 2. If JWT fails, it might be an opaque Better Auth session token
    if token_data is None:
        print(f"DEBUG: JWT verification failed, trying Session verification for: {token[:15]}...")
        token_data = AuthUtils.verify_session(token, session)
        
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - Neural Link Failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Try lookup by ID (token_data.id contains 'sub' value which is the User ID in Better Auth)
    statement = select(User).where(User.id == token_data.id)
    user = session.exec(statement).first()
    if user is None:
        print(f"DEBUG: User not found in DB for ID: {token_data.id}")
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