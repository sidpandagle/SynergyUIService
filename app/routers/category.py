from typing import List
from fastapi import Depends, APIRouter, HTTPException, File, UploadFile
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Category, Code
from app.database import get_db
from pydantic import BaseModel
import os

from app.routers.code import GetCode


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

# @router.get("/code_count")
# async def get_category_code_count(db: Session = Depends(get_db)):
#     category_list = (
#         db.query(Category)
#         .filter(Category.status == "active")
#         .order_by(Category.id.asc())
#         .all()
#     )
#     result_list = []
#     for category in category_list:
#         result_list.append({
#             'category': category.title,
#             'code_count': len(category.codes)
#         })

#     return {"data": result_list}


@router.get("/code_count")
async def get_category_code_count(db: Session = Depends(get_db)):
    # Using a subquery to get the counts in a more efficient way
    subquery = (
        db.query(
            Code.category_id,
            func.count().label("code_count")
        )
        .group_by(Code.category_id)
        .subquery()
    )

    # Join the subquery with Category to get the title and filter by status
    result_list = (
        db.query(Category.id, Category.title, subquery.c.code_count)
        .outerjoin(subquery, Category.id == subquery.c.category_id)
        .filter(Category.status == "active")
        .order_by(Category.id.asc())
        .all()
    )

    return {"data": [{"id":id, "category": title, "code_count": count} for id, title, count in result_list]}

@router.get("/{category_id}")
async def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    categoryData = (
        db.query(Category)
        .filter(Category.id == category_id, Category.status == "active")
        .first()
    )
    return {"category_id": categoryData.id, "category_title": categoryData.title, "codes": categoryData.codes}


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
