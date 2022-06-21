import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}


# 내가 파일을 불러주었을 때, 이 부분이 알아서 실행이 되었다
# `uvicorn main.app --reload` 와 동일함
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# 하지만 다른 파일이 main을 import했을 땐 실행되지 않는다
