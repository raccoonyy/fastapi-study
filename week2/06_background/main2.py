from colorama import Back
from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()


def write_log(message: str):
    with open("log2.txt", mode="a") as log:
        log.write(message)


def get_query(background_task: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_task.add_task(write_log, message)


@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}


# `BackgroundTasks`도 starlette의 `background`를 그대로 활용
# 좀더 무거운 계산을 돌려야 한다면 Celery를 추천함
