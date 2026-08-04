# @Author: LeonSong
# @Date:   2026-08-03 16:15
# @Description: Router of process methods and process options

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from api.deps import get_current_user, require_admin
from db.session import get_db
from models.users import Users
from schemas.business import (
    ProcessMethodCreate,
    ProcessMethodInfo,
    ProcessMethodUpdate,
    ProcessOptionCreate,
    ProcessOptionInfo,
    ProcessOptionUpdate,
)
from service.business import (
    create_process_method,
    create_process_option,
    delete_process_method,
    delete_process_option,
    get_process_method_by_id,
    get_process_methods,
    get_process_option_by_id,
    get_process_options,
    update_process_method,
    update_process_option,
)

router = APIRouter(prefix="/process-methods", tags=["Process"])


@router.get("/", response_model=list[ProcessMethodInfo])
async def list_process_methods(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Depends(get_current_user)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    """获取处理方式列表"""
    return get_process_methods(session, skip, limit)


@router.post("/", response_model=ProcessMethodInfo, status_code=status.HTTP_201_CREATED)
async def create_process_method_info(
    session: Annotated[Session, Depends(get_db)],
    process_method_create: ProcessMethodCreate,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """创建处理方式"""
    return create_process_method(session, process_method_create, current_user.id)


@router.get("/{process_method_id}", response_model=ProcessMethodInfo)
async def get_process_method_info(
    session: Annotated[Session, Depends(get_db)],
    process_method_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """获取指定处理方式"""
    return get_process_method_by_id(session, process_method_id)


@router.patch("/{process_method_id}", response_model=ProcessMethodInfo)
async def update_process_method_info(
    session: Annotated[Session, Depends(get_db)],
    process_method_id: int,
    process_method_update: ProcessMethodUpdate,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """更新处理方式"""
    return update_process_method(
        session, process_method_id, process_method_update, current_user.id
    )


@router.delete("/{process_method_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_process_method_info(
    session: Annotated[Session, Depends(get_db)],
    process_method_id: int,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """删除处理方式"""
    delete_process_method(session, process_method_id)


@router.get("/{process_method_id}/options", response_model=list[ProcessOptionInfo])
async def list_process_options(
    session: Annotated[Session, Depends(get_db)],
    process_method_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    """获取指定处理方式下的处理选项列表"""
    return get_process_options(session, process_method_id, skip, limit)


@router.post(
    "/{process_method_id}/options",
    response_model=ProcessOptionInfo,
    status_code=status.HTTP_201_CREATED,
)
async def create_process_option_info(
    session: Annotated[Session, Depends(get_db)],
    process_method_id: int,
    process_option_create: ProcessOptionCreate,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """在指定处理方式下创建处理选项"""
    return create_process_option(
        session, process_method_id, process_option_create, current_user.id
    )


@router.get(
    "/{process_method_id}/options/{process_option_id}", response_model=ProcessOptionInfo
)
async def get_process_option_info(
    session: Annotated[Session, Depends(get_db)],
    process_method_id: int,
    process_option_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """获取指定处理选项"""
    return get_process_option_by_id(session, process_method_id, process_option_id)


@router.patch(
    "/{process_method_id}/options/{process_option_id}", response_model=ProcessOptionInfo
)
async def update_process_option_info(
    session: Annotated[Session, Depends(get_db)],
    process_method_id: int,
    process_option_id: int,
    process_option_update: ProcessOptionUpdate,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """更新指定处理选项"""
    return update_process_option(
        session,
        process_method_id,
        process_option_id,
        process_option_update,
        current_user.id,
    )


@router.delete(
    "/{process_method_id}/options/{process_option_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_process_option_info(
    session: Annotated[Session, Depends(get_db)],
    process_method_id: int,
    process_option_id: int,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """删除指定处理选项"""
    delete_process_option(session, process_method_id, process_option_id)
