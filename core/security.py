# @Author: LeonSong
# @Date:   2026-07-31 11:07
# @Description: Password hash and verify

from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from core.config import settings

password_hash = PasswordHash.recommended()

# openssl rand -base64 32
JWT_KEY = settings.JWT_KEY


def hash_password(passwd: str) -> str:
    """hash user's password"""
    return password_hash.hash(passwd)


def verify_password(password: str, hashed_password):
    """verify the password"""
    return password_hash.verify(password, hashed_password)


def get_access_token(user_id: str):
    """get jwt token"""
    now = datetime.now(UTC)
    payload = {
        "sub": user_id,
        "iat": int(now.timestamp()),
        "exp": int(
            (now + timedelta(hours=settings.JWT_ACCESS_TOKEN_DURATION)).timestamp()
        ),
    }
    return jwt.encode(payload, JWT_KEY, algorithm="HS256")


def parse_jwt_token(token: str):
    """parse jwt token info"""
    payload = jwt.decode(token, JWT_KEY, algorithms="HS256")
    return payload
