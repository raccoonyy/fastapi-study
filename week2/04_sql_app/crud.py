# Create, Read, Update, Delete
# 사용자 한 명을 읽는다
# 사용자 목록을 읽는다
# 아이템 목록을 읽는다
# 사용자를 생성한다
# 아이템을 생성한다

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)  # 데이터를 담은 SQLAlchemy 모델 인스턴스를 생성
    db.add(db_user)      # 인스턴스를 DB 세션에 추가(add)
    db.commit()          # 세션의 변경 사항을 데이터베이스에 적용
    db.refresh(db_user)  # 인스턴스의 변경 사항을 리로드 - db_user.id 같은 것
    return db_user       # 리로드한 인스턴스를 반환


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# DB에서 한 가지 일을 담당하는 함수를 여기에 만들면 됨.
# API 함수와 분리하는 편이 좋음. 유닛테스트하기도 쉽고.