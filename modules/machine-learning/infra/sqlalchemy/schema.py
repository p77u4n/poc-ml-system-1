from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DMTask(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True)
    result = Column(String)
    reason = Column(String)
    status = Column(String(16))
    command = Column(String(16))
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    input = Column(String)


class DMUser(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
