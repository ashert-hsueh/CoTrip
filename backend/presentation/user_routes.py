from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from application.user_service import UserService
from database.user_database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/users", tags=["users"])

# 请求模型
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UpdateUsernameRequest(BaseModel):
    user_id: int
    new_username: str

class UpdatePasswordRequest(BaseModel):
    user_id: int
    old_password: str
    new_password: str

# 注册用户
@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    result = user_service.register_user(request.username, request.email, request.password)
    if not result["success"]:
        print(f"注册失败: {result['message']}, 请求参数: {request.model_dump()}")
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# 登录用户
@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    result = user_service.login_user(request.email, request.password)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# 更新用户名
@router.put("/update-username")
async def update_username(request: UpdateUsernameRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    result = user_service.update_username(request.user_id, request.new_username)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# 更新密码
@router.put("/update-password")
async def update_password(request: UpdatePasswordRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    result = user_service.update_password(request.user_id, request.old_password, request.new_password)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result
