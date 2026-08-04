# @Author: LeonSong
# @Date:   2026-07-29 19:00
# @Description:

from fastapi import FastAPI

import models  # noqa: F401
from api import clients, orders, outbound_records, processes, schedules, units, users

app = FastAPI()

app.include_router(clients.router)
app.include_router(orders.router)
app.include_router(outbound_records.router)
app.include_router(processes.router)
app.include_router(schedules.router)
app.include_router(units.router)
app.include_router(users.router)


@app.get("/")
def welcome():
    return {"message": "Welcome to Qilin Manage System v0.1.0."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
