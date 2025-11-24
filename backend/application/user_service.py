from persistence.user_repository import UserRepository
from sqlalchemy.orm import Session
import bcrypt
import re
from fastapi import HTTPException, status

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def hash_password(self, password: str) -> str:
        """对密码进行哈希处理"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def check_password_strength(self, password: str) -> bool:
        """检查密码强度
        要求：
        - 至少8位，最多20位
        - 包含特殊字符、大写字母、小写字母、数字中的任意三种
        """
        if len(password) < 8 or len(password) > 20:
            return False
        
        # 检查是否包含特殊字符
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        # 检查是否包含大写字母
        has_upper = bool(re.search(r'[A-Z]', password))
        # 检查是否包含小写字母
        has_lower = bool(re.search(r'[a-z]', password))
        # 检查是否包含数字
        has_digit = bool(re.search(r'[0-9]', password))
        
        # 计算满足的条件数量
        conditions_met = sum([has_special, has_upper, has_lower, has_digit])
        
        return conditions_met >= 3
    
    def register_user(self, username: str, email: str, password: str):
        """注册用户"""
        # 检查邮箱是否已存在
        if self.repository.check_email_exists(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
        
        # 检查用户名是否已存在
        if self.repository.check_username_exists(username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已被使用"
            )
        
        # 检查密码强度
        if not self.check_password_strength(password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="密码强度不足，需要至少8位，最多20位，并包含特殊字符、大写字母、小写字母、数字中的任意三种"
            )
        
        # 哈希密码
        password_hash = self.hash_password(password)
        
        # 创建用户
        return self.repository.create_user(username, email, password_hash)
    
    def login_user(self, email: str, password: str):
        """用户登录"""
        # 通过邮箱查找用户
        user = self.repository.get_user_by_email(email)
        
        if not user or not self.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
    
    def update_username(self, user_id: int, new_username: str):
        """更新用户名"""
        # 检查新用户名是否已被使用
        existing_user = self.repository.get_user_by_username(new_username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已被使用"
            )
        
        # 更新用户名
        return self.repository.update_username(user_id, new_username)
    
    def update_password(self, user_id: int, old_password: str, new_password: str):
        """更新密码"""
        # 获取用户信息
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 验证原密码
        if not self.verify_password(old_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="原密码错误"
            )
        
        # 检查新密码强度
        if not self.check_password_strength(new_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="新密码强度不足，需要至少8位，最多20位，并包含特殊字符、大写字母、小写字母、数字中的任意三种"
            )
        
        # 哈希新密码并更新
        new_password_hash = self.hash_password(new_password)
        return self.repository.update_password(user_id, new_password_hash)
    
    def get_user_by_id(self, user_id: int):
        """通过ID获取用户信息"""
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        return user
