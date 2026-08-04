# @Author: LeonSong
# @Date:   2026-08-04
# @Description: Router of order attachments

from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from api.deps import get_current_user, require_admin
from core.enum import AttachmentType
from db.session import get_db
from models.users import Users
from schemas.business import OrderAttachmentInfo
from service.attachment import (
    create_order_attachment,
    delete_order_attachment,
    get_attachment_file_path,
    get_order_attachment_by_id,
    get_order_attachments,
)

router = APIRouter(prefix="/orders/{order_id}/attachments", tags=["Attachment"])


@router.get("/", response_model=list[OrderAttachmentInfo])
async def list_order_attachments(
    session: Annotated[Session, Depends(get_db)],
    order_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
    attachment_type: AttachmentType | None = None,
):
    """获取订单附件列表"""
    return get_order_attachments(session, order_id, attachment_type)


@router.post(
    "/", response_model=OrderAttachmentInfo, status_code=status.HTTP_201_CREATED
)
async def upload_order_attachment(
    session: Annotated[Session, Depends(get_db)],
    order_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
    attachment_type: Annotated[AttachmentType, Form()],
    file: Annotated[UploadFile, File()],
):
    """上传订单附件"""
    return create_order_attachment(
        session, order_id, attachment_type, file, current_user.id
    )


@router.get("/{attachment_id}", response_model=OrderAttachmentInfo)
async def get_order_attachment_info(
    session: Annotated[Session, Depends(get_db)],
    order_id: int,
    attachment_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """获取指定订单附件信息"""
    return get_order_attachment_by_id(session, order_id, attachment_id)


@router.get("/{attachment_id}/file")
async def get_order_attachment_file(
    session: Annotated[Session, Depends(get_db)],
    order_id: int,
    attachment_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """获取指定订单附件文件"""
    attachment = get_order_attachment_by_id(session, order_id, attachment_id)
    file_path = get_attachment_file_path(attachment)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment file did not exists",
        )
    return FileResponse(
        path=file_path, media_type=attachment.content_type, filename=attachment.filename
    )


@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_attachment_info(
    session: Annotated[Session, Depends(get_db)],
    order_id: int,
    attachment_id: int,
    current_user: Annotated[Users, Depends(require_admin)],
):
    """删除订单附件"""
    delete_order_attachment(session, order_id, attachment_id)
