from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    DateTime
)
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from datetime import datetime
from .config import engine

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(32), nullable=False, unique=True)
    password = Column(String(32), nullable=False, unique=False)
    username = Column(String(32), nullable=False, unique=False)
    email = Column(String, nullable=True, unique=True)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(Integer, nullable=False, unique=False)
    title = Column(String(100), nullable=True, unique=False)
    content = Column(String(255), nullable=True, unique=False)
    tags = Column(String(255), nullable=True, unique=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, nullable=False, unique=False)
    author = Column(Integer, nullable=False, unique=False)
    content = Column(String(255), nullable=True, unique=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

# при импорте создается БД
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


