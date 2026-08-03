# @Author: LeonSong
# @Date:   2026-08-03 16:13
# @Description: Routers of users

from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/")
async def welcome():
    return {"users": "Hello"}
