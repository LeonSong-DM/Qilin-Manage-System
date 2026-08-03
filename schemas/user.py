# @Author: LeonSong
# @Date:   2026-07-31 13:47
# @Description: User operation schemas


from pydantic import BaseModel, Field, SecretStr

from core.enum import UserRole, UserStatus


class UserCreate(BaseModel):
    """user create schema"""

    name: str = Field(min_length=1, max_length=16)
    phone_number: str = Field(
        ..., min_length=11, max_length=11, pattern=r"^1[3-9]\d{9}$"
    )
    hashed_password: SecretStr
    role: UserRole
    status: UserStatus = Field(default=UserStatus.NORMAL)


class UserLogin(BaseModel):
    phone_number: str = Field(min_length=11, max_length=11)
    password: SecretStr
