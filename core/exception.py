# @Author: LeonSong
# @Date:   2026-07-31 22:00
# @Description: Exception classes

import json

from schemas.user import UserCreate


class BusinessException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class UserExistedException(BusinessException):
    def __init__(self, user_create: UserCreate) -> None:
        info = {
            "username": user_create.name,
            "phone_number": user_create.phone_number,
            "user_role": user_create.role.value,
            "user_status": user_create.status.value,
        }
        super().__init__(json.dumps(info, indent=4, ensure_ascii=False))
