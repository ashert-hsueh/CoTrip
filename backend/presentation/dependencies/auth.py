from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from application.security.jwt import JWTToken
from application.user_service import UserService
from database import get_db
from sqlalchemy.orm import Session

# OAuth2密码Bearer令牌方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> int:
    """
    获取当前用户ID的依赖函数
    从JWT token中解析用户信息，并验证用户是否存在
    """
    # 验证JWT token
    payload = JWTToken.verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 获取用户ID
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌中缺少用户ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 验证用户是否存在
    user_service = UserService(db)
    try:
        user_id = int(user_id)
        user = user_service.user_repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的用户ID格式",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id
