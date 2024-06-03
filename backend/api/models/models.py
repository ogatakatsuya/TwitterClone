from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from api.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(1024))
    password = Column(String(1024))
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    
    posts = relationship("Post", back_populates="user")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(200))
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id', name="fk_posts_users"), nullable=False)
    user = relationship("User", back_populates="posts")

