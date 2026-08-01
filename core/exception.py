# -*- coding: utf-8 -*-
# @Author: LeonSong
# @Date:   2026-07-31 22:00
# @Description: Exception classes


class BusinessException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class OrderExistedException(BusinessException):
    def __init__(self, order_number: str) -> None:
        super().__init__(f"Order {order_number} has existed")


class OutboundRecordExistedException(BusinessException):
    def __init__(self, outbound_number: str) -> None:
        super().__init__(f"Outbound record {outbound_number} has existed")


class UnitExistedException(BusinessException):
    def __init__(self, unit_name: str) -> None:
        super().__init__(f"Unit {unit_name} has existed")


class ProcessMethodExistedException(BusinessException):
    def __init__(self, method_name: str) -> None:
        super().__init__(f"Process method {method_name} has existed")


class ProcessOptionExistedException(BusinessException):
    def __init__(self, option_name: str) -> None:
        super().__init__(f"Process option {option_name} has existed")


class ClientExistedException(BusinessException):
    def __init__(self, client_number: str) -> None:
        super().__init__(f"Client {client_number} has existed")
