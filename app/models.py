from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, server_default="active")
    created_at = Column(DateTime, server_default=func.now())

class Code(Base):
    __tablename__ = "code"

    id = Column(Integer, primary_key=True, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    title = Column(String, nullable=False)
    code = Column(String, nullable=False)
    status = Column(String, server_default="active")
    created_at = Column(DateTime, server_default=func.now())
