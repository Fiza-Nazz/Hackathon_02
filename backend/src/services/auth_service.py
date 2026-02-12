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

def verify_scrypt_password(password: str, stored_hash: str) -> bool:
    """
    Verify a password against a Scrypt hash in 'salt:hash' format (used by Better Auth).
    """
    import hashlib
    import binascii
    
    try:
        if ":" not in stored_hash:
            return False
            
        salt_hex, hash_hex = stored_hash.split(":")
        salt = binascii.unhexlify(salt_hex)
        
        # Better Auth defaults: N=16384, r=8, p=1, key_len=64
        derived_hash = hashlib.scrypt(
            password.encode(),
            salt=salt,
            n=16384,
            r=8,
            p=1,
            dklen=64
        )
        return binascii.hexlify(derived_hash).decode() == hash_hex
    except Exception as e:
        print(f"DEBUG: Scrypt verification error: {str(e)}")
        return False

# JWT settings
def get_secret_key():
    return os.getenv("BETTER_AUTH_SECRET") or "my_ultra_secure_secret_123"

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
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password using either Bcrypt (Passlib) or Scrypt (Better Auth).
        """
        # 1. Try Scrypt (Better Auth format: 'salt:hash')
        if ":" in hashed_password and len(hashed_password) > 100:
            return verify_scrypt_password(plain_password, hashed_password)
            
        # 2. Fallback to Bcrypt (New system format)
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False

    @staticmethod
    def verify_token(token: str) -> Optional[TokenData]:
        """
        Verify a JWT token and return the token data.
        Compatible with Better Auth JWT structure.
        """
        current_secret = get_secret_key()
        
        try:
            # Check if token looks like a JWT (3 parts separated by dots)
            if token.count('.') != 2:
                print(f"DEBUG: Token parts count mismatch: {token.count('.') + 1}. Token: {token[:10]}...")
                return None

            print(f"DEBUG: Attempting decode with secret: {current_secret[:5]}... alg: {ALGORITHM}")
            payload = jwt.decode(
                token, 
                current_secret, 
                algorithms=[ALGORITHM],
                options={"verify_aud": False, "verify_iss": False}
            )
            print(f"DEBUG: Token decoded successfully. Payload: {payload}")
            
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return TokenData(id=user_id)
        except JWTError as e:
            print(f"DEBUG: JWT Verification failed: {str(e)}")
            return None
        except Exception as e:
            print(f"DEBUG: Unexpected error in verify_token: {str(e)}")
            return None


    @staticmethod
    def verify_session(session_token: str, db_session: Session) -> Optional[TokenData]:
        """
        Ultra-Deep Session Search - Checks ID and Token columns
        """
        try:
            s_token = session_token.strip()
            from ..models.session import AuthSession
            
            # Better Auth sometimes uses the ID as the bearer token
            # Check both columns to be absolutely sure
            statement = select(AuthSession).where(
                (AuthSession.token == s_token) | (AuthSession.id == s_token)
            )
            result = db_session.exec(statement).first()
            
            if not result:
                print(f"CRITICAL: Token '{s_token[:10]}...' not found in any session column.")
                return None
                
            # Timezone-aware expiry check
            from datetime import timezone
            now = datetime.now(timezone.utc)
            expires_at = result.expiresAt
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
                
            if expires_at < now:
                return None
                
            return TokenData(id=result.userId)
        except Exception as e:
            print(f"ERROR in verify_session: {str(e)}")
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