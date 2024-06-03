from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from api.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(1024), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), server_default=datetime.now(), nullable=False)
    
    posts = relationship("Post", back_populates="user")
    password = relationship("Password", back_populates="user")
    
class Password(Base):
    __tablename__ = "password"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(1024), nullable=False)
    
    user_id = Column(Integer, ForeignKey('users.id', name="user_password"), nullable=False)
    user = relationship("User", back_populates="password")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(200))
    created_at = Column(DateTime, default=datetime.now(), server_default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), server_default=datetime.now(), onupdate=datetime.now(), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id', name="fk_posts_users"), nullable=False)
    user = relationship("User", back_populates="posts")

