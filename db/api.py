from typing import Sequence
import contextlib
import json

from sqlalchemy import (
    Column,
    Integer,
    String,
    and_,
    func,
    or_,
    select,
    update,
)
from sqlalchemy.orm import (
    Session
)

from .models import User, Post, Comment

def create_user(
    session: Session,
    login: str,
    password: str,
    username: str,
    email: str | None = None,
) -> User:
    user = User(
        login=login,
        password=password,
        username=username,
        email=email,
    )
    session.add(user)
    session.commit()
    return user

def add_post(
    session: Session,
    author: int,
    title: str,
    content: str, 
    tags: str | None = None,
) -> Post:
    post = Post(
        author=author,
        title=title,
        content=content,
        tags=tags
    )
    session.add(post)
    session.commit()
    return post

def add_comment(
    session: Session,
    post_id: int,
    author: int,
    content: str | None = None,
) -> Comment:
    comment = Comment(
        post_id=post_id,
        author=author,
        content=content,
    )
    session.add(comment)
    session.commit()
    return comment

def get_user_by_id(
    session: Session,
    user_id: int,
) -> User | None:

    user = session.get(User, user_id)
    return user

def get_user_by_login(
    session: Session,
    user_login: str,
) -> User | None:
    stmt = select(User).where(func.lower(User.login) == func.lower(user_login))
    user = session.scalar(stmt)

    return user

def get_user_by_login1(
    session: Session,
    user_login: str,
) -> dict | None:
    stmt = select(User.id, User.username, User.login, User.email).where(func.lower(User.login) == func.lower(user_login))
    user = session.scalar(stmt)
    print(user)
    #q = dict((cur.description[i][0], value) for i, value in enumerate(user))
    return user#{'id': id, 'login': login, 'username': username, 'email': email}

def get_users(
    session: Session,
) -> Sequence[User]:
    stmt = (
        select(User)
    )
    users = session.scalars(stmt).all()
    return users

def get_posts_by_id(
    session: Session,
    author_id: int,
) -> Sequence[Post]:
    stmt = select(Post).where(func.lower(Post.author) == func.lower(author_id))
    posts = session.scalars(stmt).all()
    return posts