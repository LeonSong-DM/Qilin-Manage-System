# @Author: LeonSong
# @Date:   2026-08-03 16:13
# @Description: Routers of users

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from api.deps import get_current_user, require_admin
from core.enum import UserRole, UserStatus
from core.exception import AuthenticationException, BusinessException
from db.session import get_db
from models.users import Users
from schemas.user import (
    LoginResponse,
    UserCreate,
    UserInfo,
    UserLogin,
    UserPasswordUpdate,
    UserUpdate,
)
from service.auth import user_authentication
from service.user import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
    update_user_password,
)

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(session: Annotated[Session, Depends(get_db)], user_login: UserLogin):
    """登录"""
    try:
        token = user_authentication(session, user_login)
    except AuthenticationException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return LoginResponse(access_token=token)


@router.get("/", response_model=list[UserInfo])
async def list_users(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Depends(require_admin)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    name: Annotated[str | None, Query(min_length=1, max_length=16)] = None,
    phone_number: Annotated[
        str | None, Query(min_length=1, max_length=11)
    ] = None,
    role: Annotated[UserRole | None, Query()] = None,
    status_filter: Annotated[UserStatus | None, Query(alias="status")] = None,
):
    """获取用户列表"""
    return get_users(
        session=session,
        skip=skip,
        limit=limit,
        name=name,
        phone_number=phone_number,
        role=role,
        status=status_filter,
    )


@router.post("/", response_model=UserInfo, status_code=status.HTTP_201_CREATED)
async def create_user_info(
    session: Annotated[Session, Depends(get_db)],
    user_create: UserCreate,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """创建用户"""
    try:
        return create_user(session, user_create, current_user.id)
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.get("/me", response_model=UserInfo)
async def get_current_user_info(
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """获取当前用户信息"""
    return current_user


@router.get("/{user_id}", response_model=UserInfo)
async def get_user_info(
    session: Annotated[Session, Depends(get_db)],
    user_id: int,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """获取指定用户信息"""
    try:
        return get_user_by_id(session, user_id)
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.patch("/{user_id}", response_model=UserInfo)
async def update_user_info(
    session: Annotated[Session, Depends(get_db)],
    user_id: int,
    user_update: UserUpdate,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """更新用户信息"""
    try:
        return update_user(session, user_id, user_update, current_user.id)
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.patch("/{user_id}/password", response_model=UserInfo)
async def update_user_password_info(
    session: Annotated[Session, Depends(get_db)],
    user_id: int,
    user_password_update: UserPasswordUpdate,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """管理员重置用户密码"""
    try:
        return update_user_password(
            session, user_id, user_password_update, current_user.id
        )
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.delete("/{user_id}", response_model=UserInfo)
async def delete_user_info(
    session: Annotated[Session, Depends(get_db)],
    user_id: int,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """禁用用户"""
    try:
        return delete_user(session, user_id, current_user.id)
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)
