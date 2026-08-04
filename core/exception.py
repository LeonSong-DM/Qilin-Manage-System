# @Author: LeonSong
# @Date:   2026-07-31 22:00
# @Description: Exception classes

import json

from fastapi import status

from schemas.user import UserCreate


class BusinessException(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "business_error"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class AuthenticationException(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "authentication_error"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class NotFoundException(BusinessException):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"


class ConflictException(BusinessException):
    status_code = status.HTTP_409_CONFLICT
    code = "conflict"


class UserExistedException(BusinessException):
    status_code = status.HTTP_409_CONFLICT
    code = "user_existed"

    def __init__(self, user_create: UserCreate) -> None:
        info = {
            "username": user_create.name,
            "phone_number": user_create.phone_number,
            "user_role": user_create.role.value,
            "user_status": user_create.status.value,
        }
        super().__init__(json.dumps(info, indent=4, ensure_ascii=False))
