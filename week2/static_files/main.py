from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# from starlette.staticfiles import StaticFiles 와 똑같음

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# mount는 자체적인 하위 경로를 관리하는 또하나의 독립적인 애플리케이션이라고 생각해야 함
# APIRouter와는 달리 완전히 독립적임
# mount한 애플리케이션은 OpenAPI 문서에 들어가지 않음
# `"/static"`: url 경로
# `directory="static"``: 스태틱 파일을 담을 디렉터리
# `name="static"`: FastAPI 내에서 사용하는 이름
