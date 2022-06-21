# 환경 구성

```shell
pip install poetry
poetry install
poetry run pytest
```

# CORS (Coss-Origin Resource Sharing)
 - 오리진?
   - 프로토콜(http | https) + 도메인 + 포트
   - [http://localhost](http://localhost)
   - [https://localhost](https://localhost)
   - [http://localhost:8000](http://localhost:8000)

 - CORS 검증 과정
   - 프론트엔드가 [http://localhost:8080](http://localhost:8080) 에 떠 있고, 백엔드(http://localhost)랑 통신하려고 한다면
        1. 브라우저는 `OPTIONS` 요청을 백엔드에 보냄 (=preflight 요청)
        1. 백엔드가 `http://localhost:8080`은 요청을 보내도 된다는 응답을 줌 (=preflight 응답)
        1. 브라우저가 JS 코드를 실행해서 실제 요청을 백엔드에 보냄
                
   - 백엔드는 요청을 받을 수 있는 오리진 주소 목록을 갖고 있어야 함 = allowed origins
   - `*`로 선언하면 다 받을 수 있음
        -   쿠키, Auth 헤더(Bearer Token 같은 거)처럼 인증 정보 들어 있는 거 빼고

 - FastAPI에서는 CORSMiddleware를 사용
   - [Starlette의 CORSMiddleware](https://www.starlette.io/middleware/#corsmiddleware)를 그대로 사용
   - [main.py 파일](03_cors/cors.py)

# SQL
 - FastAPI + SQLAlchemy + PostgreSQL 예제: [https://github.com/tiangolo/full-stack-fastapi-postgresql/](https://github.com/tiangolo/full-stack-fastapi-postgresql/)

 - ORM
   - 데이터베이스를 객체로 표현하려는 시도
   - 여기서는 SQLAlchemy를 사용

 - 코드 구조
    ```
    ── sql_app
        ├── __init__.py
        ├── crud.py
        ├── database.py
        ├── models.py
        └── schemas.py
    ```
            
   - [database.py 파일](04_sql_app/database.py)
   - [models.py 파일](04_sql_app/models.py)
   - [schemas.py 파일](04_sql_app/schemas.py)
   - `orm_mode = True` 옵션
     - 이걸 켜두면 API 정의할 때 response\_model에 pydantic 모델을 넣을 수 있음
     - 이 옵션이 없으면 연관 모델의 데이터를 불러오지 않음.
   - [crud.py 파일](04_sql_app/crud.py)
   - [main.py 파일](04_sql_app/main.py)

 - 마이그레이션 관리도구 Alembic
   - 테이블을 한 번 구성한 이후 필드나 모델 추가 등을 코드로 관리할 수 있게 도와주는 도구
   - 여기서는 다루지 않을게요

 - 마이그레이션
   - SQLAlchemy 관련 코드를 별도 코드로 빼두었다면, FastAPI와는 무관하게 Almebic으로 관리할 수 있음.
   - 백그라운드 작업 등에서 SQLAlchemy 관련 코드를 사용할 때도 FastAPI 설치 안 해도 됨.

 - 미들웨어
   - 모든 요청 전이나 후에 작업을 추가할 수 있음
   - [main.py 파일](04_sql_app/main.py) 수정해보기
   - 의존성 주입할 때는 yield가 대개의 경우 더 좋다.
   - yield 방식은 FastAPI 최신 버전에 추가됐음

# 대규모 애플리케이션
 - Flask's Blueprints랑 같은 거

 - 예시 디렉터리 구조
    ```shell
    ├── app
    │   ├── __init__.py
    │   ├── main.py
    │   ├── dependencies.py
    │   └── routers
    │   │   ├── __init__.py
    │   │   ├── items.py
    │   │   └── users.py
    │   └── internal
    │       ├── __init__.py
    │       └── admin.py
    ```

 - 파이썬 패키징
   - `__init__.py` 파일이 존재하는 디렉터리를 파이썬 패키지로 인식 가능 (= import 가능)
   - 위 예시에서 `app`은 패키지. 따라서 `import app.main` 혹은 `import app.dependencies` 가능
   - `routers` 역시 패키지. `import app.routers` 혹은 `import app.routers.items` 가능.
   - `users.py`에서 `dependencies.py`를 참조하려면 `from ...dependencies import something` 처럼.

# APIRouter
 - 패키지를 다른 FastAPI 앱과 분리하고 싶을 때 사용
    ```python
    from fastapi import APIRouter
        
    router = APIRouter()
    ```
        
 - [users.py 파일](05_bigger_app/routers/users.py)

 - `APIRouter()`는 **작은 FastAPI()** 라고 보면 됨.

 - **부록: (예시를 위한) 의존성 추가**
   - [dependencies.py 파일](05_bigger_app/dependencies.py)
   - [main.py 파일](05_bigger_app/main.py)

 - `APIRouter`는 마운트되지 않고, 따라서 애플리케이션에서 격리되지도 않습니다. OpenAPI 스키마나 사용자 인터페이스에 path 조작부(path operations)를 집어넣고 싶었기 때문입니다. path 조작부는 복제(cloned)되며, 직접 인클루드되지 않습니다.
 - 한 엔드포인트를 `/api/v1`과 `/api/latest`에 모두 등록하고 싶다면, `include_router()`를 두 번 넣고, prefix를 바꿔주세요. 흔한 경우는 아닐테지만 필요한 경우도 있더라고요.
 - 한 `APIRouter`에 또다른 `APIRouter`를 등록할 수도 있습니다.

# 백그라운드 태스크
 - [background/main.py 파일](06_background/main.py)
 - [background/main2.py 파일](06_background/main2.py)

# Meatdata
 - OpenAPI 문서를 꾸며보자
 - 옵션

| name            | type  | desc.                         |
|------------------|------|-------------------------------|
| title            | str  | API 제목                      |
| description      | str  | API 요약 설명                 |
| version          | str  | ex. 2.5.0                     |
| terms_of_service | str  | API 사용 약관 URL             |
| contact          | dict | name: str url: str email: str |
| license_info     | dict | name: str url: str            |

 - [main.py 파일](07_metadata/main.py)
 - [main2.py 파일](07_metadata/main2.py)
 - [main3.py 파일](07_metadata/main3.py)

# Static 파일
 - [main.py 파일](https:github.com/raccoonyy/fastapi-study/blob/main/week2/static_files/main.py)
