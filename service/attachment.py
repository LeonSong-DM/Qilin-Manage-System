# @Author: LeonSong
# @Date:   2026-08-04
# @Description: Service of order attachments

import secrets
import string
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core.config import settings
from core.enum import AttachmentType
from core.exception import BusinessException
from models.order_attachments import OrderAttachments
from models.orders import Orders

ALLOWED_IMAGE_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_ATTACHMENTS_PER_TYPE = 3


def get_attachment_root() -> Path:
    """获取附件根目录"""
    return Path(settings.ATTACHMENTS_DIR_ROOT)


def get_order_by_id(session: Session, order_id: int) -> Orders:
    """通过 ID 获取订单"""
    order = session.get(Orders, order_id)

    if order is None:
        raise BusinessException(f"Order {order_id} did not exists")

    return order


def validate_image_file(file: UploadFile) -> str:
    """校验上传文件是允许的图片类型，并返回扩展名"""
    if file.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        raise BusinessException("Only jpeg, png and webp images are allowed")

    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_IMAGE_EXTENSIONS:
        raise BusinessException("Only jpg, jpeg, png and webp files are allowed")

    if suffix == ".jpeg":
        return ".jpg"
    return suffix


def get_order_attachments(
    session: Session,
    order_id: int,
    attachment_type: AttachmentType | None = None,
):
    """获取订单附件列表"""
    get_order_by_id(session, order_id)
    stmt = select(OrderAttachments).where(OrderAttachments.order_id == order_id)

    if attachment_type is not None:
        stmt = stmt.where(OrderAttachments.attachment_type == attachment_type)

    stmt = stmt.order_by(OrderAttachments.id)
    return session.execute(stmt).scalars().all()


def get_order_attachment_by_id(
    session: Session, order_id: int, attachment_id: int
) -> OrderAttachments:
    """获取指定订单附件，并校验归属订单"""
    get_order_by_id(session, order_id)
    attachment = session.get(OrderAttachments, attachment_id)

    if attachment is None:
        raise BusinessException("Attachment did not exists")

    if attachment.order_id != order_id:
        raise BusinessException("Attachment does not belong to order")

    return attachment


def get_attachment_file_path(attachment: OrderAttachments) -> Path:
    """获取附件文件绝对路径"""
    return get_attachment_root() / attachment.path


def ensure_attachment_limit(
    session: Session, order_id: int, attachment_type: AttachmentType
) -> None:
    """校验订单指定类型附件数量不超过上限"""
    stmt = (
        select(func.count())
        .select_from(OrderAttachments)
        .where(
            OrderAttachments.order_id == order_id,
            OrderAttachments.attachment_type == attachment_type,
        )
    )
    attachment_count = session.execute(stmt).scalar_one()
    if attachment_count >= MAX_ATTACHMENTS_PER_TYPE:
        raise BusinessException("Each attachment type supports at most 3 images")


def random_suffix(length: int = 3) -> str:
    """生成文件名随机后缀"""
    alphabet = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def build_attachment_filename(
    order: Orders, attachment_type: AttachmentType, suffix: str
) -> str:
    """构造附件文件名"""
    return f"{order.order_number}_{attachment_type.value}_{suffix}"


def allocate_attachment_path(
    order: Orders, attachment_type: AttachmentType, extension: str
) -> tuple[str, str, Path]:
    """分配附件文件名和路径"""
    order_dir = get_attachment_root() / order.order_number
    order_dir.mkdir(parents=True, exist_ok=True)

    for _ in range(20):
        filename = f"{build_attachment_filename(order, attachment_type, random_suffix())}{extension}"
        file_path = order_dir / filename
        if not file_path.exists():
            relative_path = str(Path(order.order_number) / filename)
            return filename, relative_path, file_path

    raise BusinessException("Can not allocate attachment filename")


def create_order_attachment(
    session: Session,
    order_id: int,
    attachment_type: AttachmentType,
    file: UploadFile,
    current_user_id: int,
) -> OrderAttachments:
    """上传订单附件"""
    order = get_order_by_id(session, order_id)
    ensure_attachment_limit(session, order_id, attachment_type)
    extension = validate_image_file(file)
    filename, relative_path, file_path = allocate_attachment_path(
        order, attachment_type, extension
    )

    try:
        with file_path.open("wb") as attachment_file:
            while chunk := file.file.read(1024 * 1024):
                attachment_file.write(chunk)

        attachment = OrderAttachments(
            order_id=order_id,
            attachment_type=attachment_type,
            filename=filename,
            path=relative_path,
            content_type=file.content_type or "application/octet-stream",
            created_by=current_user_id,
            updated_by=current_user_id,
        )
        session.add(attachment)
        session.commit()
        session.refresh(attachment)
        return attachment
    except Exception:
        session.rollback()
        if file_path.exists():
            file_path.unlink()
        raise


def delete_order_attachment(
    session: Session, order_id: int, attachment_id: int
) -> None:
    """删除订单附件"""
    attachment = get_order_attachment_by_id(session, order_id, attachment_id)
    file_path = get_attachment_file_path(attachment)

    try:
        session.delete(attachment)
        session.commit()
    except Exception:
        session.rollback()
        raise

    if file_path.exists():
        file_path.unlink()
