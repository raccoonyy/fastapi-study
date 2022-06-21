import time

from fastapi import FastAPI, Request

app = FastAPI()


# http 요청에 대한 미들웨어
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()                 # 요청 전 처리
    response = await call_next(request)      # 요청 처리
    process_time = time.time() - start_time  # 요청 후 처리
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 응답 헤더에 사용자 지정 헤더를 넣고 싶으면 X-로 시작함
@app.get("/")
async def main():
    return {"message": "Hello World"}
