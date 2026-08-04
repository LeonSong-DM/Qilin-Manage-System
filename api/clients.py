# @Author: LeonSong
# @Date:   2026-08-03 16:16
# @Description: Router of Clients

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from api.deps import get_current_user, require_admin
from core.exception import BusinessException
from db.session import get_db
from models.users import Users
from schemas.business import ClientCreate, ClientInfo, ClientUpdate
from service.business import (
    create_client,
    get_client_by_id,
    get_clients,
    update_client,
)

router = APIRouter(prefix="/clients", tags=["Client"])


@router.get("/", response_model=list[ClientInfo])
async def list_clients(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Depends(get_current_user)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    client_name: Annotated[str | None, Query(min_length=1, max_length=64)] = None,
    contact_phone_number: Annotated[
        str | None, Query(min_length=1, max_length=11)
    ] = None,
):
    """获取客户列表"""
    return get_clients(
        session=session,
        skip=skip,
        limit=limit,
        client_name=client_name,
        contact_phone_number=contact_phone_number,
    )


@router.post("/", response_model=ClientInfo, status_code=status.HTTP_201_CREATED)
async def create_client_info(
    session: Annotated[Session, Depends(get_db)],
    client_create: ClientCreate,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """创建客户"""
    try:
        return create_client(session, client_create, current_user.id)
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.get("/{client_id}", response_model=ClientInfo)
async def get_client_info(
    session: Annotated[Session, Depends(get_db)],
    client_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """获取指定客户"""
    try:
        return get_client_by_id(session, client_id)
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.patch("/{client_id}", response_model=ClientInfo)
async def update_client_info(
    session: Annotated[Session, Depends(get_db)],
    client_id: int,
    client_update: ClientUpdate,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """更新客户"""
    try:
        return update_client(session, client_id, client_update, current_user.id)
    except BusinessException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)
