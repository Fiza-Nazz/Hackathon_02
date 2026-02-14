from sqlmodel import Session, select
from backend.src.database.database import engine
from backend.src.models.user import User, Account
from backend.src.services.auth_service import pwd_context

def check_user(email: str):
    with Session(engine) as session:
        print(f"Checking user: {email}")
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            print("User NOT found in auth_user table.")
            return
        
        print(f"User found: ID={user.id}, Email={user.email}")
        
        accounts = session.exec(select(Account).where(Account.userId == user.id)).all()
        print(f"Found {len(accounts)} accounts for this user.")
        
        for i, acc in enumerate(accounts):
            print(f"Account {i+1}: ID={acc.id}, Provider={acc.providerId}, HasPassword={'Yes' if acc.password else 'No'}")
            if acc.password:
                print(f"  Password hash: {acc.password[:15]}...")

if __name__ == "__main__":
    check_user("abub96891@gmail.com")
