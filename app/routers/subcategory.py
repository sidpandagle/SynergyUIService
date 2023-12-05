from typing import List
from fastapi import Depends, APIRouter, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.models import Subcategory
from app.database import get_db
from pydantic import BaseModel
import os


class CreateSubcategory(BaseModel):
    title: str
    category_id: int


class GetSubcategory(BaseModel):
    id: int
    title: str
    category_id: int
    status: str
    created_at: str


class UpdateSubcategory(BaseModel):
    id: int
    title: str
    category_id: int


class DeleteSubcategory(BaseModel):
    id: int
    status: str


router = APIRouter()


@router.get("/")
async def get_subcategory(db: Session = Depends(get_db)):
    subcategory_list = (
        db.query(Subcategory)
        .filter(Subcategory.status == "active")
        .order_by(Subcategory.id.asc())
        .all()
    )
    return {"data": subcategory_list}


@router.get("/{subcategory_id}")
async def get_subcategory_by_id(subcategory_id: int, db: Session = Depends(get_db)):
    subcategoryData = (
        db.query(Subcategory)
        .filter(Subcategory.id == subcategory_id, Subcategory.status == "active")
        .first()
    )
    return {"data": subcategoryData}


@router.post("/")
async def create_subcategory(category: CreateSubcategory, db: Session = Depends(get_db)):
    db_subcategory = Subcategory(**category.dict())
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)

    return {"data": "Subcategory Added Successfully"}


@router.put("/")
async def update_subcategory(new_subcategory: UpdateSubcategory, db: Session = Depends(get_db)):
    existing_subcategory = (
        db.query(Subcategory).filter(Subcategory.id == new_subcategory.id).first()
    )
    if existing_subcategory is None:
        raise HTTPException(status_code=404, detail="SubCategory not found")

    for attr, value in new_subcategory.dict().items():
        setattr(existing_subcategory, attr, value)

    db.commit()
    db.refresh(existing_subcategory)

    return {"data": existing_subcategory}


@router.delete("/{subcategory_id}")
async def delete_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    existing_subcategory = db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
    if existing_subcategory is None:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    setattr(existing_subcategory, "status", "inactive")

    db.commit()
    db.refresh(existing_subcategory)

    return {"data": existing_subcategory}
