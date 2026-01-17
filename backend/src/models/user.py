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

    def __setattr__(self, name, value):
        if name == 'updatedAt':
            super().__setattr__('updatedAt', datetime.utcnow())
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
    id: str
    createdAt: datetime
    updatedAt: datetime