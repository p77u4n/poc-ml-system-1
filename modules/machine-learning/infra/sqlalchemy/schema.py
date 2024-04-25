from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True)
    result = Column(String)
    reason = Column(String)
    status = Column(String(10))
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
