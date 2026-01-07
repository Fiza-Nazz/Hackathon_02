from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
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
    """
    User model representing a registered user with email, password hash,
    account creation date, and authentication tokens.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

    def __setattr__(self, name, value):
        if name == 'updated_at':
            super().__setattr__('updated_at', datetime.utcnow())
        super().__setattr__(name, value)


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
    id: int
    created_at: datetime
    updated_at: datetime