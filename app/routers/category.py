from typing import List
from fastapi import Depends, APIRouter, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.models import Category
from app.database import get_db
from pydantic import BaseModel
import os

router = APIRouter()

@router.get("/")
async def get_category(db: Session = Depends(get_db)):
    category_list = db.query(Category).order_by(Category.id.asc()).all()
    return {"data": category_list}

@router.get("/{category_id}")
async def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    categoryData = db.query(Category).filter(Category.id == category_id).first()
    return {"data": categoryData}
