import databases
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URL = "postgresql+asyncpg://postgres:buzzni-assignment@postgres-user:5432"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = create_async_engine(DATABASE_URL)
Session = scoped_session(sessionmaker())

Base = declarative_base()
