from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# 데이터베이스 테이블 생성하기
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 의존성 주입용
def get_db():
    db = SessionLocal()  # database.py에서 선언했던 녀석
    # 각 요청마다 세션, 연결은 독립적으로 생성됨. 한 요청 안에서는 유지되고. 
    # 요청 끝나면 사라짐.
    try:
        yield db
    finally:
        db.close()
# try - finally로 처리하면 요청 처리 중에 익셉션이 발생해도 세션이 잘 닫힘.
# 하지만 500 에러 이외의 익셉션을 발생시킬 수는 없음. 이건 나중에 미들웨어에서 수정하기로 하자.


# # 아래는 미들웨어 설명할 때 
# @app.middleware("http")
# async def db_session_middleware(request: Request, call_next):
#     response = Response("Internal server error", status_code=500)
#     try:
#         request.state.db = SessionLocal()
#         response = await call_next(request)
#     finally:
#         request.state.db.close()
#     return response
# # 이 방식이 기존보다 조금 복잡하긴 하다
# # 미들웨어는 async 함수여야 한다.
# #   만약 await 걸린 부분을 추가한다면 성능이 좀 떨어지겠죠.
# #   SQLAlchemy 관련 작업에서 큰 문제는 아니겠지만요.
# #   I/O 대기 작업을 많이 넣으면 문제가 많이 되겠고요.
# # 미들웨어는 모든 요청에 대해 실행됨
# #   DB 연결이 필요 없는 경우에도!
#
#
# def get_db(request: Request):
#     return request.state.db
# # request.state은 Starlette의 Reqeust state임.
# # 여기서는 한 요청 안에서 세션을 공유하려고 사용.


# Depends(get_db)를 사용해서 데이터베이스에 대한 의존성을 주입함
# 실제 리턴하는 값들은 SQLAlchemy의 인스턴스지만, 
# response_model에는 Pydantic 모델을 적어둠. (orm_mode = True를 기억해요.)
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# 여기서는 async def 말고 그냥 def를 사용함.
# 데이터베이스와 비동기적으로 통신하고 싶다면 Async SQL Databases 문서를 참고하세요.
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
