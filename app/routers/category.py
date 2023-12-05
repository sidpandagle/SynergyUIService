from typing import List
from fastapi import Depends, APIRouter, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.models import Category
from app.database import get_db
from pydantic import BaseModel
import os


class CreateCategory(BaseModel):
    title: str


class GetCategory(BaseModel):
    id: int
    title: str
    status: str
    created_at: str


class UpdateCategory(BaseModel):
    id: int
    title: str


class DeleteCategory(BaseModel):
    id: int
    status: str


router = APIRouter()


@router.get("/")
async def get_category(db: Session = Depends(get_db)):
    category_list = (
        db.query(Category)
        .filter(Category.status == "active")
        .order_by(Category.id.asc())
        .all()
    )
    return {"data": category_list}


@router.get("/{category_id}")
async def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    categoryData = (
        db.query(Category)
        .filter(Category.id == category_id, Category.status == "active")
        .first()
    )
    return {"data": categoryData}


@router.post("/")
async def create_category(category: CreateCategory, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return {"data": "Category Added Successfully"}

@router.put("/")
async def update_category(new_category: UpdateCategory, db: Session = Depends(get_db)):
    existing_category = (
        db.query(Category).filter(Category.id == new_category.id).first()
    )
    if existing_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    for attr, value in new_category.dict().items():
        setattr(existing_category, attr, value)

    db.commit()
    db.refresh(existing_category)

    return {"data": existing_category}


@router.delete("/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    existing_category = db.query(Category).filter(Category.id == category_id).first()
    if existing_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    setattr(existing_category, "status", "inactive")

    db.commit()
    db.refresh(existing_category)

    return {"data": existing_category}
