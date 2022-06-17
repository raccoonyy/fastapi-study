from fastapi import FastAPI, Depends
from .dependencies import get_query_token, get_token_header

from .internal import admin
from .routers import items, users  # 앞에서 만든 라우터를 이렇게 import해서
# from .routers.items import router  라고 하지 않는 이유는
# from .routers.users import router  랑 겹치기 때문
# from .internal.admin import router 도 있고

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)  # 이렇게 추가
app.include_router(items.router)
# 아래처럼 router를 선언하지 않고 include_router에서 설정해도 됩니다.
# 이렇게 하면 admin.py 파일을 수정하지 않고도 다른 프로젝트에서 재활용할 수 있다고...
# (ex. 인증 체계가 다른, 어떤 프로젝트에서 재활용한다든가.)
# 왜냐하면 라우터 설정이 이 app에만 적용되니까.
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
# 라우터 추가하면서 성능 걱정은 하지 않아도 됩니다.
# 마이크로초 정도가 걸릴 뿐이예요.
# (=그것보단 ~느린~ 니 로직을 신경쓰렴)

@app.get("/")  # 여전히 예전 방식으로 path 지정할 수도 있고
async def main():
    return {"message": "Hello Bigger Applications!"}
