from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .models.user import UserCreate, UserLogin, UserUpdate, TokenData
from database.entities.user import User
from persistence.user_repository import UserRepository
import re

# 配置
SECRET_KEY = "your-secret-key-here"  # 实际应用中应该从环境变量获取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def get_current_user(self, token: str) -> Optional[User]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        user = self.get_user_by_email(email=token_data.email)
        if user is None:
            raise credentials_exception
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repository.get_user_by_email(email=email)



    def register_user(self, user: UserCreate) -> Optional[User]:
        # 检查密码是否匹配
        if user.password != user.confirm_password:
            return None
        
        # 检查邮箱是否已存在
        existing_user = self.user_repository.get_user_by_email(user.email)
        if existing_user:
            return None
        
        # 检查用户名是否已存在
        existing_username = self.user_repository.get_user_by_username(user.username)
        if existing_username:
            return None
        
        # 创建用户
        hashed_password = self.get_password_hash(user.password)
        return self.user_repository.create_user(user, hashed_password)

    def login_user(self, user: UserLogin) -> Optional[str]:
        # 检查用户是否存在
        db_user = self.user_repository.get_user_by_email(user.email)
        if not db_user:
            return None
        
        # 检查密码是否正确
        if not self.verify_password(user.password, db_user.hashed_password):
            return None
        
        # 生成访问令牌
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": db_user.email},
            expires_delta=access_token_expires
        )
        return access_token

    def update_user_username(self, user_id: int, new_username: str) -> Optional[UserRepository]:
        # 检查新用户名是否已存在
        existing_username = self.user_repository.get_user_by_username(new_username)
        if existing_username and existing_username.id != user_id:
            return None
        
        # 更新用户名
        return self.user_repository.update_user_username(user_id, new_username)

    def update_user_password(self, user_id: int, current_password: str, new_password: str, confirm_new_password: str) -> Optional[UserRepository]:
        # 检查新密码是否匹配
        if new_password != confirm_new_password:
            return None
        
        # 检查新密码强度
        if not self.validate_password_strength(new_password):
            return None
        
        # 检查原密码是否正确
        user = self.user_repository.get_user_by_id(user_id)
        if not user or not self.verify_password(current_password, user.hashed_password):
            return None
        
        # 更新密码
        new_hashed_password = self.get_password_hash(new_password)
        return self.user_repository.update_user_password(user_id, new_hashed_password)
