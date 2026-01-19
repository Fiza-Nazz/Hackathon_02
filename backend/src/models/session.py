from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class AuthSession(SQLModel, table=True):
    __tablename__ = "auth_session"
    id: str = Field(primary_key=True)
    userId: str = Field(foreign_key="auth_user.id", nullable=False)
    expiresAt: datetime = Field(nullable=False)
    token: str = Field(nullable=False)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    ipAddress: Optional[str] = None
    userAgent: Optional[str] = None
