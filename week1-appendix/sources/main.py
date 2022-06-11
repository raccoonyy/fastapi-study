from fastapi import FastAPI, Header, HTTPException, Depends

from . import schemas, models
from .database import Session

app = FastAPI()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=list[schemas.User])
async def get_users(user_token: str = Header(alias="USER-TOKEN"), db: Session = Depends(get_db)):
    # user = models.get_user_by_token(db=db, user_token=user_token)
    # if not user:
    #     raise HTTPException(status_code=401)
    return models.get_users(db=db)


@app.get("/me", response_model=schemas.User)
async def me(user_token: str = Header(alias="USER-TOKEN"), db: Session = Depends(get_db)):
    user = models.get_user_by_token(db=db, user_token=user_token)
    if not user:
        raise HTTPException(status_code=404)

    return user

'''
HEADER 인증 빼고 해보자

테스트코드

기본 CRUD를 만들자

서로 통신 어떻게?
'''
