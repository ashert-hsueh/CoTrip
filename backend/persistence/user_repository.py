from database.user_database import UserDatabase
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, db: Session):
        self.db = UserDatabase(db)
    
    def create_user(self, username: str, email: str, password_hash: str):
        """创建用户"""
        user_data = {
            "username": username,
            "email": email,
            "password_hash": password_hash
        }
        return self.db.create_user(user_data)
    
    def get_user_by_email(self, email: str):
        """通过邮箱获取用户"""
        return self.db.get_user_by_email(email)
    
    def get_user_by_username(self, username: str):
        """通过用户名获取用户"""
        return self.db.get_user_by_username(username)
    
    def get_user_by_id(self, user_id: int):
        """通过ID获取用户"""
        return self.db.get_user_by_id(user_id)
    
    def update_username(self, user_id: int, new_username: str):
        """更新用户名"""
        return self.db.update_user(user_id, {"username": new_username})
    
    def update_password(self, user_id: int, new_password_hash: str):
        """更新密码"""
        return self.db.update_user(user_id, {"password_hash": new_password_hash})
    
    def check_email_exists(self, email: str):
        """检查邮箱是否已存在"""
        return self.db.get_user_by_email(email) is not None
    
    def check_username_exists(self, username: str):
        """检查用户名是否已存在"""
        return self.db.get_user_by_username(username) is not None
