# @Author: LeonSong
# @Date:   2026-07-29 21:14
# @Description: Outbound order Model

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, TimeStampMixin


class OutBoundRecord(TimeStampMixin, Base):
    __tablename__ = "out_bound_order"

    #  出库编号: QLOUTYYYYMMDDXXX
    outbound_record_id: Mapped[str] = mapped_column(String(12), primary_key=True)
    order_id: Mapped[str] = mapped_column(String(12), nullable=False)
    outbound_count: Mapped[int] = mapped_column(Integer(), nullable=False)
    outbound_unit: Mapped[str] = mapped_column(String(), nullable=False)

    outbound_weight: Mapped[float] = mapped_column(Float(), nullable=False)
    outbound_user_id: Mapped[str] = mapped_column(String(), nullable=False)

    outbound_img1_path: Mapped[str] = mapped_column(String(), nullable=False)
    outbound_img2_path: Mapped[str] = mapped_column(String(), nullable=False)
    outbound_img3_path: Mapped[str] = mapped_column(String(), nullable=False)

    is_document_recycled: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=False
    )
    document_img_path: Mapped[str] = mapped_column(String(), default=None)
