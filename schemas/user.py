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
    password: SecretStr
    role: UserRole
    status: UserStatus = Field(default=UserStatus.NORMAL)


class UserUpdate(BaseModel):
    name: str | None = Field(min_length=1, max_length=16, default=None)
    phone_number: str | None = Field(
        min_length=11, max_length=11, pattern=r"^1[3-9]\d{9}$", default=None
    )
    role: UserRole | None = None
    status: UserStatus | None = None


class UserPasswordUpdate(BaseModel):
    password: SecretStr


class UserSelfPasswordUpdate(BaseModel):
    old_password: SecretStr
    new_password: SecretStr


class UserLogin(BaseModel):
    phone_number: str = Field(min_length=11, max_length=11, examples=["13800000001"])
    password: SecretStr = Field(examples=["admin123456"])


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInfo(BaseModel):
    id: int
    user_number: str
    name: str
    phone_number: str
    role: UserRole
    status: UserStatus

    model_config = {"from_attributes": True}
