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
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
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
    email: Optional[str] = None


class AuthUtils:
    """
    Authentication utilities for password hashing and token management.
    """

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Generate a hash for a plain password.
        """
        return pwd_context.hash(password)

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.
        """
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if not user or not AuthUtils.verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """
        Create a JWT access token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[TokenData]:
        """
        Verify a JWT token and return the token data.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return None
            token_data = TokenData(email=email)
        except JWTError:
            return None
        return token_data

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
        statement = select(User).where(User.email == token_data.email)
        user = session.exec(statement).first()
        if user is None:
            raise credentials_exception
        return user