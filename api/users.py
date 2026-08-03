# @Author: LeonSong
# @Date:   2026-08-03 16:13
# @Description: Routers of users

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.exception import AuthenticationException
from db.session import get_db
from schemas.user import LoginResponse, UserLogin
from service.auth import user_authentication

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/")
async def welcome():
    return {"users": "Hello"}


@router.post("/login")
async def login(session: Annotated[Session, Depends(get_db)], user_login: UserLogin):
    try:
        token = user_authentication(session, user_login)
    except AuthenticationException:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return LoginResponse(access_token=token, code=status.HTTP_200_OK)
