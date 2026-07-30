# @Author: LeonSong
# @Date:   2026-07-30 20:43
# @Description: Model of attachments

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, TimeStampMixin


class OrderAttachments(TimeStampMixin, Base):
    __tablename__ = "order_attachment"

    # attachment id: QLAYYYYMMDDXXX
    id: Mapped[str] = mapped_column(String(14), primary_key=True)
    type: Mapped[str] = mapped_column(String(32))
    path: Mapped[str] = mapped_column(String(255))
    order_id: Mapped[str] = mapped_column(String(16))
