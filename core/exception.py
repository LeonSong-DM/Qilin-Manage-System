# -*- coding: utf-8 -*-
# @Author: LeonSong
# @Date:   2026-07-31 22:00
# @Description: Exception classes


class BusinessException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
