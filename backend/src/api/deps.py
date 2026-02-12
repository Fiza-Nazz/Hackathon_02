from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional
from ..database.database import get_session
from ..services.auth_service import AuthUtils
from ..models import User


security = HTTPBearer(auto_error=False)

def get_current_user(
    request: Request,
    session: Session = Depends(get_session),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """
    Ultra-Resilient User Retrieval with Full Header Analytics
    """
    # LOG ALL HEADERS FOR DEBUGGING
    print("--- NEURAL LINK HEADER ANALYTICS ---")
    for name, value in request.headers.items():
        if name.lower() == "authorization":
            print(f"HEADER: {name}: Bearer {value[7:15]}...") # Partial for security
        else:
            print(f"HEADER: {name}: {value}")
    
    token = credentials.credentials if credentials else None
    
    if not token:
        print("DEBUG: CRITICAL - No token found in credentials object.")
        # Fallback: check raw headers manually
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            print("DEBUG: Token recovered from raw headers.")
            
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # 1. Try JWT verification (Speed tier)
    token_data = AuthUtils.verify_token(token)
    
    # 2. Deep Database Search (Failsafe tier)
    if token_data is None:
        token_data = AuthUtils.verify_session(token, session)
        
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session not found or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Final User Resolution
    statement = select(User).where(User.id == token_data.id)
    user = session.exec(statement).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User Identity Lost")
        
    return user


def get_auth_utils():
    """
    Get authentication utilities for dependency injection.
    """
    return AuthUtils()