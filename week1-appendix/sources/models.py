from sqlalchemy import Column, Integer, String, select, Sequence
from sqlalchemy.orm import Session

from sources.database import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String)
    access_token = Column(String)


def get_user(db: Session, user_id: int):
    with db as session:
        query = select(User).where(User.id == user_id)
        result = session.execute(query)

    return result.first()


def get_users(db: Session):
    with db as session:
        query = select(User)
        result = session.execute(query, execution_options={"prebuffer_rows": True})

    return result.scalars().all()


def get_user_by_token(db: Session, user_token: str):
    with db as session:
        query = select(User).where(User.access_token == user_token)
        result = session.execute(query)
    return result.scalars().first()
