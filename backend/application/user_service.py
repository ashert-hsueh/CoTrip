from typing import Optional
from passlib.context import CryptContext
from database.entities.user import User
from persistence.user_repository import UserRepository

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """获取密码哈希值"""
        return pwd_context.hash(password)
    
    def validate_password_strength(self, password: str) -> tuple[bool, str]:
        """验证密码强度"""
        # 长度检查
        if len(password) < 8 or len(password) > 20:
            return False, "密码长度必须在8-20位之间"
        
        # 检查复杂度（需要至少三种字符类型）
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        complexity_count = sum([has_upper, has_lower, has_digit, has_special])
        
        if complexity_count < 3:
            return False, "密码必须包含至少三种字符类型（大写字母、小写字母、数字、特殊字符）"
        
        return True, ""
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """用户认证"""
        user = self.user_repository.get_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        return user
    
    def create_user(self, username: str, email: str, password: str) -> tuple[Optional[User], str]:
        """创建用户"""
        # 检查邮箱是否已存在
        if self.user_repository.get_by_email(email):
            return None, "邮箱已被注册"
        
        # 检查用户名是否已存在
        if self.user_repository.get_by_username(username):
            return None, "用户名已被使用"
        
        # 验证密码强度
        is_valid, error_msg = self.validate_password_strength(password)
        if not is_valid:
            return None, error_msg
        
        # 创建用户
        hashed_password = self.get_password_hash(password)
        user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )
        
        return self.user_repository.create(user), ""
    
    def update_username(self, user_id: int, new_username: str) -> tuple[bool, str]:
        """更新用户名"""
        # 检查新用户名是否已存在
        existing_user = self.user_repository.get_by_username(new_username)
        if existing_user and existing_user.id != user_id:
            return False, "用户名已被使用"
        
        # 更新用户名
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False, "用户不存在"
        
        user.username = new_username
        self.user_repository.update(user)
        return True, ""
    
    def update_password(self, user_id: int, old_password: str, new_password: str) -> tuple[bool, str]:
        """更新密码"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False, "用户不存在"
        
        # 验证旧密码
        if not self.verify_password(old_password, user.password_hash):
            return False, "原密码错误"
        
        # 验证新密码强度
        is_valid, error_msg = self.validate_password_strength(new_password)
        if not is_valid:
            return False, error_msg
        
        # 更新密码
        user.password_hash = self.get_password_hash(new_password)
        self.user_repository.update(user)
        return True, ""