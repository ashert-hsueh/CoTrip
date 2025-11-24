from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from database.user_database import get_db
from persistence.user_repository import UserRepository
from application.user_service import UserService
from application.auth import Token, create_access_token, verify_token, TokenData

router = APIRouter(prefix="/api/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token, credentials_exception)
    user_repository = UserRepository(db)
    user = user_repository.get_by_email(token_data.email)
    
    if user is None:
        raise credentials_exception
    return user


@router.api_route("/register", methods=["GET", "POST", "OPTIONS"])
def register(username: str = None, email: str = None, password: str = None, db: Session = Depends(get_db)):
    """用户注册"""
    # 处理OPTIONS请求
    from fastapi.responses import Response
    if not all([username, email, password]):
        return Response(status_code=200)
    
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    user, error_msg = user_service.create_user(username, email, password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    return {"message": "注册成功", "user_id": user.id}


@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """用户登录"""
    # OAuth2PasswordRequestForm使用username字段，但我们用邮箱登录
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    user = user_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建访问令牌
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/update-username")
def update_username(new_username: str, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """更新用户名"""
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    success, error_msg = user_service.update_username(current_user.id, new_username)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    return {"message": "用户名更新成功"}


@router.put("/update-password")
def update_password(old_password: str, new_password: str, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """更新密码"""
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    success, error_msg = user_service.update_password(current_user.id, old_password, new_password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    return {"message": "密码更新成功"}


@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    """获取当前用户信息"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }