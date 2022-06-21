from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DB 주소 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# SQLAlchemy의 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # SQLite Only!
)

# 아직 진짜 세션은 아니고 세션을 만들 수 있는 객체.
# SQLAlchemy의 Session과 구분하려고 SessionLocal이라고 이름 붙임.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델이나 클래스를 Base 기반으로 생성
Base = declarative_base()
