from sqlalchemy.orm import Session
from database.user_database import UserDatabase
from application.models.user import UserCreate, UserUpdate
from database.entities.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        self.user_db = UserDatabase(db)

    def create_user(self, user: UserCreate, hashed_password: str) -> User:
        return self.user_db.create_user(user, hashed_password)

    def get_user_by_email(self, email: str) -> User:
        return self.user_db.get_user_by_email(email)

    def get_user_by_username(self, username: str) -> User:
        return self.user_db.get_user_by_username(username)

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_db.get_user_by_id(user_id)

    def update_user_username(self, user_id: int, new_username: str) -> User:
        return self.user_db.update_user_username(user_id, new_username)

    def update_user_password(self, user_id: int, new_hashed_password: str) -> User:
        return self.user_db.update_user_password(user_id, new_hashed_password)

    def delete_user(self, user_id: int) -> bool:
        return self.user_db.delete_user(user_id)
