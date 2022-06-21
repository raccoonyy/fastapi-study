from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# pydantic으로 모델 하나를 생성
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    # pydantic 모델은 이렇게 사용
    return User(
        username=token + "fakedecoded", email="test@test.net", full_name="Alan Kim"
    )


# oauth2_scheme를 의존
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # 만약 데이터베이스나 외부 API라면 await를 걸어야겠죠?
    user = fake_decode_token(token)
    return user


# get_current_user를 의존. (get_current_user는 oauto2_scheme을 의존)
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# request body도 pydantic이었다는 거 기억합시다

# Check! 이런 식으로 의존 관계를 걸어서, User 모델을 리턴하는 서로 다른 의존 관계를 사용할 수도 있음
# The way this dependency system is designed allows us to have different dependencies (different "dependables") that all return a User model.
# We are not restricted to having only one dependency that can return that type of data.
