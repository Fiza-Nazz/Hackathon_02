from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel
import uuid
from datetime import datetime, timezone

from ..database.database import get_session
from ..models.user import User, Account, UserCreate
from ..services.auth_service import AuthUtils, pwd_context, jwt, get_secret_key, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, Token

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, session: Session = Depends(get_session)):
    # 1. Check if user exists
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    # 2. Create User
    user_id = str(uuid.uuid4())
    new_user = User(
        id=user_id,
        email=user_data.email,
        createdAt=datetime.now(timezone.utc),
        updatedAt=datetime.now(timezone.utc)
    )
    session.add(new_user)
    
    # 3. Create Account (for password storage)
    hashed_password = pwd_context.hash(user_data.password)
    new_account = Account(
        id=str(uuid.uuid4()),
        userId=user_id,
        accountId=user_data.email,
        providerId="credential",
        password=hashed_password,
        createdAt=datetime.now(timezone.utc),
        updatedAt=datetime.now(timezone.utc)
    )
    session.add(new_account)
    
    session.commit()
    session.refresh(new_user)

    # 4. Generate JWT
    secret = get_secret_key()
    access_token = jwt.encode(
        {"sub": user_id}, 
        secret, 
        algorithm=ALGORITHM
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, session: Session = Depends(get_session)):
    print(f"DEBUG: Login attempt for email: {login_data.email}")
    
    # 1. Find User
    statement = select(User).where(User.email == login_data.email)
    user = session.exec(statement).first()
    if not user:
        print(f"DEBUG: User not found for email: {login_data.email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    print(f"DEBUG: User found: {user.id}")

    # 2. Find Credential Account and check password
    acc_statement = select(Account).where(Account.userId == user.id).where(Account.providerId == "credential")
    account = session.exec(acc_statement).first()
    
    if not account:
        print(f"DEBUG: No account found for user ID: {user.id}")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not account.password:
        print(f"DEBUG: Account found but has no password (maybe Social login?)")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    print(f"DEBUG: Password hash in DB: {account.password[:10]}...")

    # 3. Check password using Hybrid Verification (Bcrypt + Scrypt)
    try:
        is_valid = AuthUtils.verify_password(login_data.password, account.password)
        print(f"DEBUG: Hybrid Password verification result: {is_valid}")
        
        if not is_valid:
            raise HTTPException(status_code=401, detail="Invalid email or password")
    except Exception as e:
        print(f"DEBUG: Password verification error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    # 4. Generate JWT
    secret = get_secret_key()
    print(f"DEBUG: Generating token for {user.id} with secret: {secret[:5]}...")
    access_token = jwt.encode(
        {"sub": user.id}, 
        secret, 
        algorithm=ALGORITHM
    )
    
    return {"access_token": access_token, "token_type": "bearer"}