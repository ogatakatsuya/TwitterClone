from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(1024))
    password = Column(String(1024))
    
    posts = relationship("Post", back_populates="user")  # Corrected class name to "Post"

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(200))

    user_id = Column(Integer, ForeignKey('users.id', name="fk_posts_users"), nullable=False)
    user = relationship("User", back_populates="posts")

