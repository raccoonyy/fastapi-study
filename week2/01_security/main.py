from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # 토큰 발급용 API는 `/token`이라고 선언
# 아주 엄격한 파이썬 개발자라면 `token_url`이라고 적고 싶을 테죠. 하지만 이렇게 한 이유는 OpenAPI 스펙 때문입니다.
# oauth2_scheme이 callable이기 때문에 Depends에 넣을 수 있음.


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):  # 보안 의존성 주입
    return {"token": token}
