# @Author: LeonSong
# @Date:   2026-07-30 21:10
# @Description: The enum classes required by the system

from enum import Enum


# 用户角色
class UserRole(Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"


class UserStatus(Enum):
    NORMAL = "normal"
    FORBIDDEN = "forbidden"


# 订单状态
class OrderStatus(Enum):
    SCHEDULING = "scheduling"  # 待排产
    FINISHED = "finished"  # 已完成（需要单据回收）


# 出库状态
class OutboundStatus(Enum):
    NOT_OUTBOUND = "not_outbound"  # 未出库
    PARTIALLY_OUTBOUND = "partially_outbound"  # 部分出库
    FULLY_OUTBOUND = "fully_outbound"  # 未出库


class AttachmentType(Enum):
    INBOUND = "inbound"  # 入库留存
    OUTBOUND = "outbound"  # 出库留存
    HARVEST = "harvest"  # 回收单据


# 优先级
class OrderPriority(Enum):
    P0 = "p0"  # 最高
    P1 = "p1"
    P2 = "p2"
    P3 = "p3"


class NumberType(Enum):
    """维护编号序列"""

    USER = "QLU"
    PRODUCTION = "QLPS"
    ATTACHMENT = "QLA"
    ORDER = "QLORD"
    OUTBOUND = "QLOUT"
    CLIENT = "QLC"


class SCHEDULE_STATUS(Enum):
    COMPLETED = "completed"
    IN_PRODUCTION = "in_production"
