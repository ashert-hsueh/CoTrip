from sqlalchemy.orm import Session
from database.entities.user_entity import UserEntity

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, username: str, email: str, hashed_password: str) -> UserEntity:
        user = UserEntity(username=username, email=email, hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_by_email(self, email: str) -> UserEntity:
        return self.db.query(UserEntity).filter(UserEntity.email == email).first()
    
    def get_user_by_username(self, username: str) -> UserEntity:
        return self.db.query(UserEntity).filter(UserEntity.username == username).first()
    
    def get_user_by_id(self, user_id: int) -> UserEntity:
        return self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
    
    def update_username(self, user_id: int, new_username: str) -> UserEntity:
        user = self.get_user_by_id(user_id)
        if user:
            user.username = new_username
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def update_password(self, user_id: int, new_hashed_password: str) -> UserEntity:
        user = self.get_user_by_id(user_id)
        if user:
            user.hashed_password = new_hashed_password
            self.db.commit()
            self.db.refresh(user)
        return user
