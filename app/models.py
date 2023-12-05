from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String)
    created_at = Column(String)

class Subcategory(Base):
    __tablename__ = "subcategory"

    id = Column(Integer, primary_key=True, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    title = Column(String, nullable=False)
    status = Column(String)
    created_at = Column(String)

class Code(Base):
    __tablename__ = "code"

    id = Column(Integer, primary_key=True, nullable=False)
    subcategory_id = Column(Integer, ForeignKey("subcategory.id"), nullable=False)
    title = Column(String, nullable=False)
    code = Column(String, nullable=False)
    status = Column(String)
    created_at = Column(String)
