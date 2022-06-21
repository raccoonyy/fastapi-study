# 환경 구성

```shell
pip install poetry
poetry install
poetry run pytest
```

# 보안

- 보안, 인증, 권한을 제어하는 방법은 많음. 대개는 복잡하고 어려운 주제.
- 다수의 프레임워크에서 이를 제어하려면 노력도 많이 들고 코드도 많이 작성함. (모든 코드의 50% 정도를 차지할 걸?)
- FastAPI는 쉽고, 빠르고 표준적인 방법으로 이를 제어할 수 있음. 보안 공부 안해도.
## 용어 정리
- OAuth2: 페이스북 로그인, 구글 로그인 같은 걸 생각해보세요.
- OAuth1: OAuth1과 이름만 비슷하고 완전 다름. 통신을 암호화하는 방식. 오늘날 많이 사용되지 않음.
  - OAuth2는 통신 암호화 왜 관심 안 둠? -> (상식적이라면) HTTPS 쓸 테니까.
- OpenID Connect: OAuth2 기반이지만 OAuth2에서 약간 애매한 부분을 명확하게 정리한 규격. 구글 로그인은 사실 OpenID Connect임. (OAuth2 방식도 여전히 지원함) <-> 페북 로그인은 OpenID Connect 지원 안 함. OAuth2만 지원.
- OpenID: (OpenID Connect가 아님에 주의) OpenID 규격 중 하나. OAuth2 기반이 아님. 요즘은 많이 안 씀.
- OpenAPI: (Swagger의 요즘 이름) API 제작에 사용하는 공개 규격. 리눅스 재단 소속. **FastAPI는 OpenAPI 기반!** -> 그래서 문서 자동으로 잘 만들어 줌.
  - OpenAPI는 보안 스키마 몇 가지를 지원함
    - `apiKey`: 쿼리 파라미터나 헤더, 쿠키로 특정 키를 받는 인증 방식
    - `http`: HTTP 기본 인증
      - `bearer`: `Authorization` 헤더에 `Bearer {KEYKEYKEY...}` 를 넘기는 인증 방식. OAuth2가 이 방식을 상속함.
    - `oauth2`: 보안을 제어하는 모든 OAuth2 방식(`flows`라고 함)
      - 다음은 OAuth 2.0 인증 프로바이더(페북, 구글 등)를 사용할 때 적합함
        - `implicit`
        - `clientCredentials`
        - `authorizationCode`
      - `flow` 중 하나는 같은 애플리케이션의 인증을 다룰 때 딱 맞음
        - `password`: 좀 있다 다룰 예정
    - `openIdConnet`: OAuth2 인증 데이터를 자동으로 찾을 방법을 제공
      - 자동 검색은 OpenID Connect 규격에 정의된 방식임.
- 인증이나 권한 제어할 때 구글, 페북, 트위터, 깃헙 등을 붙이기가 엄청 쉬움. 복잡한 건 **FastAPI**가 알아서 해줄게
- `fastapi.security`를 잘 사용해보렴

## 첫 예시
- 백엔드 API가 어떤 도메인에 존재하고
- 프론트엔드는 별도 도메인으로 구성됨 (아니면 같은 도메인의 다른 패스나 모바일 애플리케이션 형태로)
- `username`과 `password`를 사용해서 프론트엔드가 백엔드와 통신하게 해보자.
- OAuth2를 사용하겠음. -> 그럼 그 긴 스펙 문서를 다 읽어야 할까? -> **FastAPI**가 알아서 해줄게.
- [main.py 파일](01_security/main.py)
- http://127.0.0.1:8000/docs 접속해서 오른쪽 상단의 Authorize 버튼 눌러보자.

## `password` flow
- OAuth2에 정의된 방식 중 하나
- OAuth2를 사용하여 서버 인증 서버와 사용자 인증 서버를 분리할 수 있음.
  - (하지만 여기선 한 애플리케이션에서 둘다 처리할 예정)

### 구현하려는 인증 흐름
- 사용자가 프론트엔드에서 `username`과 `password`를 입력
- 프론트엔드는 `username`, `password`를 백엔드 API에 보냄. (`tokenUrl="token"`로 지정하여, API 주소가 `/token`이라고 선언함)
- API는 `username`, `password`를 확인한 후 "token"을 응답
  - token은 사용자를 구분할 수 있는 문자열
  - 일반적으로 token은 일정 기간이 지난 후 만료됨
    - token 만료시 사용자는 재로그인해야 함
    - 토큰이 탈취되더라도 영구적이지 않기 때문에 위험이 덜 함
- 프론트엔드는 token을 저장(브라우저 캐시, 로컬 스토리지 등)
- 사용자가 프론트엔드의 다른 화면으로 이동
- 프론트엔드는 다른 API에서 데이터 받아옴
  - 데이터를 받아오려면 인증이 필요함
  `- Authorization` 헤더에 `Bearer {token}`을 넣어서 전달

## OAuth2PasswordBearer
- 정리하면, Bearer 토큰을 사용하여 Password 플로우의 OAuth2를 구현함. = `OAuth2PasswordBearer`가 해주는 일임.
  - (더 복잡한 경우가 생기기 전까지는 Bearer 토큰 방식만으로도 충분할 거임)
- `OAuth2PasswordBearer` 스키마는 `fastapi.security.oauth2.OAuth2` 상속 -> `fastapi.security.base.SecurityBase` 상속
- `SecurityBase` 상속한 클래스가 의존성에 들어오면 FastAPI가 알아서 API 만들고, 인증도 붙여 줌.

## 현재 사용자 파악하기
- [main2.py 파일](01_security/main2.py)
``` shell
field = ModelField(name='body', type=Body_login_token_post, required=True)

    def check_file_field(field: ModelField) -> None:
        field_info = field.field_info
        if isinstance(field_info, params.Form):
            try:
                # __version__ is available in both multiparts, and can be mocked
                from multipart import __version__  # type: ignore
    
                assert __version__
                try:
                    # parse_options_header is only available in the right multipart
                    from multipart.multipart import parse_options_header  # type: ignore
    
                    assert parse_options_header
                except ImportError:
                    logger.error(multipart_incorrect_install_error)
                    raise RuntimeError(multipart_incorrect_install_error)
            except ImportError:
                logger.error(multipart_not_installed_error)
>               raise RuntimeError(multipart_not_installed_error)
E               RuntimeError: Form data requires "python-multipart" to be installed. 
E               You can install "python-multipart" with: 
E               
E               pip install python-multipart

.venv/lib/python3.10/site-packages/fastapi/dependencies/utils.py:108: RuntimeError
--------------------------------------------------- Captured log call ---------------------------------------------------
ERROR    fastapi:utils.py:107 Form data requires "python-multipart" to be installed. 
You can install "python-multipart" with: 

pip install python-multipart
```

- `python-multipart` 설치해주세요

## username과 password를 실제로 확인하기
### OAuth2 규격
- OAuth2 규격의 `password` 플로우는 `username`과 `password`만 확인함. `user-name`이나 `email` 등은 작동하지 않음
- **scope**
  - `username`, `password` 외에 `scope` 필드를 넘길 수도 있음.
  - 빈 칸으로 구분된 문자열
  - 권한을 관리할 때 사용함
  - 예)
    - 일반 `users:read`, `users:write`,
    - 페북, 인스타그램 `instagram_basic`()
    - 구글 `https://www.googleapis.com/auth/drive`
- 원래 OAuth2 규격은 `grant_type`도 받음. 만약 이걸 강제하고 싶다면 `OAuth2PasswordRequestForm`이 아닌 `OAuth2PasswordRequestFormStrict`를 사용할 것
- `OAuth2PasswordRequestForm`은 `OAuth2PasswordBearer` 용도가 아닌 곳에서도 사용 가능
- `OAuth2PasswordRequestForm`은 원래의 `scope` 대신 빈 칸 기준으로 분리한 `scopes` 배열을 갖고 있음
- [01_security/main3.py] 파일
- http://127.0.0.1:8000/docs 접속해서 오른쪽 상단의 Authorize 버튼 눌러보자.
  - johndoe / secret 정보로 로그인해보기
  - 브라우저에서 `/users/me`도 접근해보자
  - 로그아웃 후에 다시 `/users/me`에 접근해보자
  - alice / secret2 정보로 로그인해보자
- 암호 해시와 관련된 글: https://d2.naver.com/helloworld/318732

## JWT 방식 구현하기
### JWT?
- Json Web Token
- 예) `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c`
- 암호화된 정보는 아니므로 누구든 정보를 추출해낼 수 있음
- 하지만 사인드(signed) 정보이므로 검증할 수는 있음.
- 정보 속에 만료기한도 설정할 수 있음. (=DB 조회 없이 토큰 유효성 + 만료 여부 확인 가능)
- python-jose 설치하세요

### 패스워드 해싱
- passlib 설치하세요
- 여러 암호 해싱 알고리즘을 제공하는데 여기서는 Bcrypt 사용하겠음
- Django나 Flask의 암호 데이터도 passlib으로 공유 가능
- [main4.py 파일](01_security/main4.py)

### JWT의 `sub` 키
- 사용하는 건 선택사항. 문자열이어야 함.
- 예시에서는 사용자 이름을 넣어두었음.
- 토큰의 카테고리(자동차, 블로그 포스팅)를 넣거나 권한(수정 가능 등)을 넣어도 됨
- 애플리케이션에서 고유한 값으로 설정해야 함.
- http://127.0.0.1:8000/docs 접속해서 오른쪽 상단의 Authorize 버튼 눌러보자.
  - 개발자 도구 열고,
  - johndoe / secret 정보로 로그인해보기
  - 브라우저에서 `/users/me`도 접근해보자
  - 요청 헤더에 JWT 토큰 들어간 것 확인하기
  - scopes는 Advanced User Guide에서 다룹니다.

# 미들웨어

- 특정 경로로 들어오는 모든 요청 전, 후에 처리하는 로직
- 사용자 요청 -> 미들웨어 -> 실제 뷰 -> 미들웨어 -> 서버 응답
- [main.py 파일](02_middleware/main.py)

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
   - [cors.py 파일](03_cors/cors.py)

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
 - [main.py 파일](08_static_files/main.py)

# 디버깅
- `if __name__ == "__main__":` 을 하면 해당 파일 실행시 자동으로 if 안의 내용이 실행됨.
- 하지만 해당 파일을 다른 파일에서 `import`하면 실행되지 않음.
- `import uvicorn`해서 `uvicorn`을 바로 실행할 수도 있음.
  ``` python
	uvicorn.run(app, host="0.0.0.0", port=8000)
  ```
- `uvicorn`을 코드로 실행했듯, 여느 파이썬 프로그램이라도 디버거에서 호출할 수 있음
- VS Code와 파이참에서 디버거로 파일 실행하기 실습
- [main.py 파일](09_debugging/main.py)
