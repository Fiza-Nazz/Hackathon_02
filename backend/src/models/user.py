from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .task import Task
    from .chatbot import Conversation
from pydantic import validator
import re


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)

    @validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
            raise ValueError('Invalid email address')
        return v.lower().strip()


class User(UserBase, table=True):
    __tablename__ = "auth_user"
    id: str = Field(primary_key=True)
    name: Optional[str] = None
    email: str = Field(unique=True, nullable=False, max_length=255)
    emailVerified: bool = Field(default=False)
    image: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship(back_populates="user")


class Account(SQLModel, table=True):
    __tablename__ = "auth_account"
    id: str = Field(primary_key=True)
    userId: str = Field(foreign_key="auth_user.id", nullable=False)
    accountId: str = Field(nullable=False)
    providerId: str = Field(nullable=False)
    accessToken: Optional[str] = None
    refreshToken: Optional[str] = None
    password: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)


class Verification(SQLModel, table=True):
    __tablename__ = "auth_verification"
    id: str = Field(primary_key=True)
    identifier: str = Field(nullable=False)
    value: str = Field(nullable=False)
    expiresAt: datetime = Field(nullable=False)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    email: str
    password: str


class UserRead(UserBase):
    """
    Schema for reading user data (without password).
    """
    id: str
    createdAt: datetime
    updatedAt: datetime