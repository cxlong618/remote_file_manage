from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import timedelta
from .security import verify_password, create_access_token, get_password_hash
from ..config import settings

router = APIRouter(prefix="/api/auth", tags=["认证"])


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str
    token_type: str = "bearer"
    username: str


class UserResponse(BaseModel):
    """用户信息响应"""
    username: str
    is_authenticated: bool = True


# 延迟哈希密码（避免模块导入时的长度限制问题）
_hashed_password = None


def get_hashed_password():
    """获取密码哈希（延迟计算）"""
    global _hashed_password
    if _hashed_password is None:
        _hashed_password = get_password_hash(settings.password)
    return _hashed_password


@router.post("/login", response_model=LoginResponse, summary="用户登录")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    用户登录接口

    - **username**: 用户名
    - **password**: 密码
    """
    # 验证用户名
    if form_data.username != settings.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 验证密码
    if not verify_password(form_data.password, get_hashed_password()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 创建访问令牌
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )

    return LoginResponse(
        access_token=access_token,
        username=form_data.username
    )


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
async def get_current_user_info():
    """
    获取当前认证用户的信息
    """
    return UserResponse(username=settings.username)
