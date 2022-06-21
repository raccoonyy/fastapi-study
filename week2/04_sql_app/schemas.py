# Pydantic model
# 데이터 유효성 검증용

from pydantic import BaseModel


class ItemBase(BaseModel):  # 모델의 공통 요소
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True  
        # 필드 선언이 아니라 모델 설정이므로 값 선언이 아닌 할당한다는 점을 주의.
        # 또, data["id"] 뿐만 아니라 data.id로도 데이터에 접근할 수 있음


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []
    # API로 주고받는 정보에는 password를 넣지 않았음!

    class Config:
        orm_mode = True


'''
!헷갈리지 말기!

SQLAlchemy의 모델 선언 방식
name = Column(String)

Pydantic의 모델 선언 방식
name: str
'''