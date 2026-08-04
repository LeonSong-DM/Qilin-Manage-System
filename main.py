# @Author: LeonSong
# @Date:   2026-07-29 19:00
# @Description:

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models  # noqa: F401
from api import (
    attachments,
    clients,
    orders,
    outbound_records,
    processes,
    schedules,
    statistics,
    units,
    users,
)
from core.config import settings
from core.exception import AuthenticationException, BusinessException
from core.handlers import authentication_exception_handler, business_exception_handler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(AuthenticationException, authentication_exception_handler)

app.include_router(attachments.router)
app.include_router(clients.router)
app.include_router(orders.router)
app.include_router(outbound_records.router)
app.include_router(processes.router)
app.include_router(schedules.router)
app.include_router(statistics.router)
app.include_router(units.router)
app.include_router(users.router)


@app.get("/")
def welcome():
    return {"message": "Welcome to Qilin Manage System v0.1.0."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
