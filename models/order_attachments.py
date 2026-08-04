# @Author: LeonSong
# @Date:   2026-07-30 20:43
# @Description: Model of attachments

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.enum import AttachmentType
from db.base import AuditMixin, Base, TimeStampMixin


class OrderAttachments(TimeStampMixin, AuditMixin, Base):
    __tablename__ = "order_attachment"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    attachment_type: Mapped[AttachmentType] = mapped_column(
        SQLEnum(AttachmentType), nullable=False
    )
    filename: Mapped[str] = mapped_column(String(128), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(64), nullable=False)
    order_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("orders.id"), nullable=False
    )

    order: Mapped["Orders"] = relationship(back_populates="attachments")
