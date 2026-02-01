from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate, UserRead
from ..services.auth_service import AuthUtils


class UserService:
    """
    Service class for user-related operations.
    """

    @staticmethod
    def create_user(session: Session, user_create: UserCreate) -> UserRead:
        """
        Create a new user with the provided details.
        """
        # Check if user already exists
        existing_user = session.exec(
            select(User).where(User.email == user_create.email)
        ).first()

        if existing_user:
            raise ValueError("User with this email already exists")

        # Hash the password
        password_hash = AuthUtils.get_password_hash(user_create.password)

        # Create the new user
        db_user = User(
            email=user_create.email,
            password_hash=password_hash
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        # Return the created user (without password hash)
        return UserRead(
            id=db_user.id,
            email=db_user.email,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Get a user by their email address.
        """
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
        """
        Get a user by their ID.
        """
        statement = select(User).where(User.id == user_id)
        return session.exec(statement).first()