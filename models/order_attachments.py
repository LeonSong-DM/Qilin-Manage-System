# @Author: LeonSong
# @Date:   2026-07-30 20:43
# @Description: Model of attachments

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, TimeStampMixin


class OrderAttachments(TimeStampMixin, Base):
    __tablename__ = "order_attachment"

    # attachment id: QLAYYYYMMDDXXX
    id: Mapped[str] = mapped_column(String())
    type: Mapped[str] = mapped_column(String())
    path: Mapped[str] = mapped_column(String())
    order_id: Mapped[str] = mapped_column(String(16))
