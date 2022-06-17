# https://github.com/tiangolo/full-stack-fastapi-postgresql/ 에 좋은 보일러플레이트가 존재함

# 여기서의 Model은 SQLAlchemy의 Model임
# Pydantic의 Model과 다름

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base  # 방금 봤던 Base!


class User(Base):  # Base는 이렇게 사용함
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # 정수형 컬럼
    email = Column(String, unique=True, index=True)     # 문자열 컬럼
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)           # 불린형 컬럼

    items = relationship("Item", back_populates="owner")  # 연관 테이블


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
