from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.database import get_db
from application.user_service import UserService, SECRET_KEY, ALGORITHM
from application.models.user import UserCreate, UserLogin, UserUpdate, UserResponse, Token, TokenData
from database.entities.user import User
from jose import JWTError, jwt

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# OAuth2 密码Bearer方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

# 依赖项：获取当前用户
def get_current_user(token: str = Depends(oauth2_scheme), user_service: UserService = Depends(get_user_service)):
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
    
    current_user = user_service.get_user_by_email(email=token_data.email)
    if current_user is None:
        raise credentials_exception
    return current_user

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    # 检查邮箱是否已存在
    existing_user_by_email = user_service.get_user_by_email(user.email)
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    
    # 检查用户名是否已存在
    existing_user_by_username = user_service.get_user_by_username(user.username)
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )
    
    # 检查密码是否匹配
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )
    
    # 创建用户
    db_user = user_service.register_user(user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create user",
        )
    
    return db_user

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login_user(user: UserLogin, user_service: UserService = Depends(get_user_service)):
    access_token = user_service.login_user(user)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/profile/username", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_username(user_update: UserUpdate, current_user: User = Depends(get_current_user), user_service: UserService = Depends(get_user_service)):
    if not user_update.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a new username",
        )
    
    updated_user = user_service.update_user_username(current_user.id, user_update.username)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    return updated_user

@router.put("/profile/password", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_password(user_update: UserUpdate, current_user: User = Depends(get_current_user), user_service: UserService = Depends(get_user_service)):
    if not user_update.current_password or not user_update.new_password or not user_update.confirm_new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide current password, new password, and confirm new password",
        )
    
    updated_user = user_service.update_user_password(
        current_user.id,
        user_update.current_password,
        user_update.new_password,
        user_update.confirm_new_password
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect, new passwords do not match, or new password is invalid",
        )
    return updated_user

@router.get("/profile", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    return current_user


