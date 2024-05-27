from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_name = Column(String(1024))
    password = Column(String(1024))