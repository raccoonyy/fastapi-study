from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


# 백그라운드 태스크는 async이든 아니든 FastAPI가 알아서 적절히 처리해준다.
# 여기서는 파일 쓰기 작업이고 여기에 async나 await을 사용하지 않을 예정이므로 그냥 def.
def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    # 실제 백그라운드를 트리거할 땐 이렇게 add_task
    background_tasks.add_task(write_notification, email, message="some noti")
    return {"message" : "Noti sent in the background"}
