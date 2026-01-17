from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session, select
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from ..models.user import User
from ..database.database import get_session
import os


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
# Use BETTER_AUTH_SECRET to match frontend Better Auth configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET") or os.getenv("SECRET_KEY", "development-secret-key-1234567890")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    """
    Token schema for JWT tokens.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Token data schema for JWT token payload.
    """
    id: Optional[str] = None


class AuthUtils:
    """
    Authentication utilities for password hashing and token management.
    """

    @staticmethod
    def verify_token(token: str) -> Optional[TokenData]:
        """
        Verify a JWT token and return the token data.
        Compatible with Better Auth JWT structure.
        """
        # Ensure we're using the latest secret from environment
        current_secret = os.getenv("BETTER_AUTH_SECRET") or os.getenv("SECRET_KEY", "development-secret-key-1234567890")
        
        try:
            # Check if token looks like a JWT (3 parts separated by dots)
            if token.count('.') != 2:
                print(f"DEBUG: Token does not follow JWT format (parts: {token.count('.') + 1})")
                return None

            # Better Auth by default uses HS256 if a secret is provided
            # We disable audience verification as Better Auth might set it to something we don't expect
            payload = jwt.decode(
                token, 
                current_secret, 
                algorithms=[ALGORITHM],
                options={"verify_aud": False, "verify_iss": False}
            )
            print(f"DEBUG: Token decoded successfully. Payload: {payload}")
            
            # Better Auth puts user ID in 'sub'
            user_id: str = payload.get("sub")
            
            if user_id is None:
                print("DEBUG: JWT verified but 'sub' claim is missing. Payload keys:", payload.keys())
                return None
            token_data = TokenData(id=user_id)
        except JWTError as e:
            print(f"DEBUG: JWT Verification failed. Secret: {current_secret[:3]}***. Error: {str(e)}")
            print(f"DEBUG: Token being verified: {token}")
            return None
        return token_data

    @staticmethod
    def verify_session(session_token: str, db_session: Session) -> Optional[TokenData]:
        """
        Verify an opaque Better Auth session token against the database.
        """
        try:
            # Query the session from the database
            from ..models.session import AuthSession
            statement = select(AuthSession).where(AuthSession.token == session_token)
            result = db_session.exec(statement).first()
            
            if not result:
                print(f"DEBUG: Session not found in DB for token: {session_token[:15]}...")
                return None
                
            # Check if session is expired
            from datetime import timezone
            now = datetime.now(timezone.utc)
            
            # Ensure result.expiresAt is aware for comparison
            expires_at = result.expiresAt
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
                
            if expires_at < now:
                print(f"DEBUG: Session expired for token: {session_token[:15]}...")
                return None
                
            print(f"DEBUG: Session verified via DB. User ID: {result.userId}")
            return TokenData(id=result.userId)
        except Exception as e:
            print(f"DEBUG: Session verification failed with error: {str(e)}")
            return None

    @staticmethod
    def get_current_user(session: Session = Depends(get_session), token: str = Depends(HTTPBearer())):
        """
        Get the current user based on the JWT token.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_data = AuthUtils.verify_token(token.credentials)
        if token_data is None:
            raise credentials_exception
        statement = select(User).where(User.id == token_data.id)
        user = session.exec(statement).first()
        if user is None:
            raise credentials_exception
        return user