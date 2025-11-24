from sqlalchemy.orm import Session
from .entities.user import User
from application.models.user import UserCreate, UserUpdate

class UserDatabase:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate, hashed_password: str) -> User:
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user_username(self, user_id: int, new_username: str) -> User:
        user = self.get_user_by_id(user_id)
        if user:
            user.username = new_username
            self.db.commit()
            self.db.refresh(user)
        return user

    def update_user_password(self, user_id: int, new_hashed_password: str) -> User:
        user = self.get_user_by_id(user_id)
        if user:
            user.hashed_password = new_hashed_password
            self.db.commit()
            self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
