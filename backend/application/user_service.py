from passlib.context import CryptContext
from persistence.user_repository import UserRepository
from sqlalchemy.orm import Session
from .security.jwt import JWTToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
    
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def register_user(self, username: str, email: str, password: str) -> dict:
        # 检查用户名是否已存在
        existing_user_by_username = self.user_repository.get_user_by_username(username)
        if existing_user_by_username:
            return {"success": False, "message": "用户名已存在"}
        
        # 检查邮箱是否已存在
        existing_user_by_email = self.user_repository.get_user_by_email(email)
        if existing_user_by_email:
            return {"success": False, "message": "邮箱已存在"}
        
        # 哈希密码
        hashed_password = self.hash_password(password)
        
        # 创建用户
        user = self.user_repository.create_user(username, email, hashed_password)
        
        return {"success": True, "message": "注册成功", "user_id": user.id}
    
    def login_user(self, email: str, password: str) -> dict:
        # 根据邮箱查找用户
        user = self.user_repository.get_user_by_email(email)
        if not user:
            return {"success": False, "message": "邮箱或密码错误"}

        # 验证密码
        if not self.verify_password(password, user.hashed_password):
            return {"success": False, "message": "邮箱或密码错误"}

        # 生成JWT token
        access_token = JWTToken.create_access_token(
            data={"sub": str(user.id), "username": user.username, "email": user.email}
        )

        return {"success": True, "message": "登录成功", "user_id": user.id, "username": user.username, "email": user.email, "access_token": access_token}
    
    def update_username(self, user_id: int, new_username: str) -> dict:
        # 检查新用户名是否已存在
        existing_user = self.user_repository.get_user_by_username(new_username)
        if existing_user and existing_user.id != user_id:
            return {"success": False, "message": "用户名已存在"}
        
        # 更新用户名
        user = self.user_repository.update_username(user_id, new_username)
        if not user:
            return {"success": False, "message": "用户不存在"}
        
        return {"success": True, "message": "用户名更新成功", "username": user.username}
    
    def update_password(self, user_id: int, old_password: str, new_password: str) -> dict:
        # 查找用户
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            return {"success": False, "message": "用户不存在"}
        
        # 验证旧密码
        if not self.verify_password(old_password, user.hashed_password):
            return {"success": False, "message": "旧密码错误"}
        
        # 哈希新密码
        hashed_new_password = self.hash_password(new_password)
        
        # 更新密码
        self.user_repository.update_password(user_id, hashed_new_password)
        
        return {"success": True, "message": "密码更新成功"}
