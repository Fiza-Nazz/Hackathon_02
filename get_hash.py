from sqlmodel import Session, select
from backend.src.database.database import engine
from backend.src.models.user import User, Account

def check_user(email: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            print("User NOT found")
            return
        
        accounts = session.exec(select(Account).where(Account.userId == user.id)).all()
        for acc in accounts:
            print(f"Account ID: {acc.id}")
            print(f"Provider: {acc.providerId}")
            print(f"Hash: {acc.password}")
            print(f"Hash Length: {len(acc.password) if acc.password else 0}")

if __name__ == "__main__":
    check_user("abub96891@gmail.com")
