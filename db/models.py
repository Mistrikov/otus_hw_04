from .database import db

from werkzeug.security import generate_password_hash,  check_password_hash
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False, unique=False)
    username = db.Column(db.String(32), nullable=False, unique=False)
    email = db.Column(db.String, nullable=False, unique=True)
    def __repr__(self):
        return self.username

    def set_password(self, passwd):
	    self.password = generate_password_hash(passwd)

    def check_password(self,  passwd):
	    return check_password_hash(self.password, passwd)
    
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.Integer, nullable=False, unique=False)
    title = db.Column(db.String(100), nullable=True, unique=False)
    content = db.Column(db.String(255), nullable=True, unique=False)
    tags = db.Column(db.String(255), nullable=True, unique=False)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, nullable=False, unique=False)
    author = db.Column(db.Integer, nullable=False, unique=False)
    content = db.Column(db.String(255), nullable=True, unique=False)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
