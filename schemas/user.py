# @Author: LeonSong
# @Date:   2026-07-31 13:47
# @Description: User operation schemas


from pydantic import BaseModel, Field

from core.enum import UserRole, UserStatus


class UserCreate(BaseModel):
    """user create schema"""

    user_number: str = Field(min_length=14, max_length=14)
    phone_number: str = Field(
        ..., min_length=11, max_length=11, pattern=r"^1[3-9]\d{9}$"
    )
    hashed_password: str = Field(...)
    role: UserRole
    status: UserStatus = Field(default=UserStatus.NORMAL)
    created_by: str = Field(..., min_length=14, max_length=14)
