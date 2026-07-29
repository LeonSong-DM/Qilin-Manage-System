# @Author: LeonSong
# @Date:   2026-07-29 19:00
# @Description:

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def welcome():
    return {"message": "Welcome to Qilin Manage System v0.1.0."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
