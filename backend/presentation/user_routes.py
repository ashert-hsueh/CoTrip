from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict, Any
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

from database.user_database import get_db
from application.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])

# JWT配置
SECRET_KEY = "your-secret-key"  # 在实际生产环境中应该使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

# 创建访问令牌
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 获取当前用户
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user_service = UserService(db)
    user = user_service.get_user_by_id(int(user_id))
    return user

# 用户注册请求模型
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

# 更新用户名请求模型
class UpdateUsernameRequest(BaseModel):
    new_username: str

# 更新密码请求模型
class UpdatePasswordRequest(BaseModel):
    old_password: str
    new_password: str

# 响应模型
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

@router.post("/register", response_model=UserResponse)
def register(user_data: Dict[str, Any], db: Session = Depends(get_db)):
    """用户注册"""
    user_service = UserService(db)
    user = user_service.register_user(
        username=user_data.get("username"),
        email=user_data.get("email"),
        password=user_data.get("password")
    )
    return user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录"""
    # OAuth2PasswordRequestForm 使用 username 字段，但我们用 email 登录
    user_service = UserService(db)
    user = user_service.login_user(email=form_data.username, password=form_data.password)
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: Any = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

@router.put("/username")
def update_username(user_data: Dict[str, Any], current_user: Any = Depends(get_current_user), db: Session = Depends(get_db)):
    """更新用户名"""
    user_service = UserService(db)
    updated_user = user_service.update_username(
        user_id=current_user.id,
        new_username=user_data.get("new_username")
    )
    return {"message": "用户名更新成功", "user": updated_user}

@router.put("/password")
def update_password(user_data: Dict[str, Any], current_user: Any = Depends(get_current_user), db: Session = Depends(get_db)):
    """更新密码"""
    user_service = UserService(db)
    user_service.update_password(
        user_id=current_user.id,
        old_password=user_data.get("old_password"),
        new_password=user_data.get("new_password")
    )
    return {"message": "密码更新成功"}
