# @Author: LeonSong
# @Date:   2026-08-03 16:13
# @Description: Routers of users

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.deps import get_current_user
from core.exception import AuthenticationException
from db.session import get_db
from models.users import Users
from schemas.user import LoginResponse, UserInfo, UserLogin
from service.auth import user_authentication

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/")
async def welcome():
    return {"users": "Hello"}


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(session: Annotated[Session, Depends(get_db)], user_login: UserLogin):
    """登录"""
    try:
        token = user_authentication(session, user_login)
    except AuthenticationException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return LoginResponse(access_token=token)


@router.get("/me", response_model=UserInfo)
async def get_current_user_info(
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """获取当前用户信息"""
    return current_user
