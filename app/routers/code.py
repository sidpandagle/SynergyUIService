from typing import List
from fastapi import Depends, APIRouter, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.models import Code
from app.database import get_db
from pydantic import BaseModel
import os


class CreateCode(BaseModel):
    title: str
    code: str
    category_id: int


class GetCode(BaseModel):
    id: int
    title: str
    code: str
    category_id: int
    status: str
    created_at: str


class UpdateCode(BaseModel):
    id: int
    title: str
    code: str
    category_id: int


class DeleteCode(BaseModel):
    id: int
    status: str


router = APIRouter()


# Get Code with Catgegory
@router.get("/")
async def get_Code(db: Session = Depends(get_db)):
    code_list = (
        db.query(Code)
        .filter(Code.status == "active")
        .order_by(Code.id.asc())
        .all()
    )
    result_list = []
    for code in code_list:
        result_list.append({
            "id": code.id,
            "title": code.title,
            "code": code.code,
            "status": code.status,
            "created_at": code.created_at,
            "category": code.category
        })

    return {"data": result_list}

# Get Codes with CatgegoryID
@router.get("/category/{category_id}")
async def get_Code_by_category_id(category_id: int, db: Session = Depends(get_db)):
    code_list = (
        db.query(Code)
        .filter(Code.status == "active" and  Code.category_id == category_id)
        .order_by(Code.id.asc())
        .all()
    )
    result_list = []
    for code in code_list:
        result_list.append({
            "id": code.id,
            "title": code.title,
            "code": code.code,
            "status": code.status,
            "created_at": code.created_at,
            "category": code.category.title
        })

    return {"data": result_list}


@router.get("/{code_id}")
async def get_Code_by_id(code_id: int, db: Session = Depends(get_db)):
    code_data = (
        db.query(Code)
        .filter(Code.id == code_id, Code.status == "active")
        .first()
    )
    return {"data": code_data}


@router.post("/")
async def create_Code(code: CreateCode, db: Session = Depends(get_db)):
    db_code = Code(**code.dict())
    db.add(db_code)
    db.commit()
    db.refresh(db_code)

    return {"data": "Code Added Successfully"}


@router.put("/")
async def update_Code(new_code: UpdateCode, db: Session = Depends(get_db)):
    existing_code = (
        db.query(Code).filter(Code.id == new_code.id).first()
    )
    if existing_code is None:
        raise HTTPException(status_code=404, detail="Code not found")

    for attr, value in new_code.dict().items():
        setattr(existing_code, attr, value)

    db.commit()
    db.refresh(existing_code)

    return {"data": existing_code}


@router.delete("/{code_id}")
async def delete_Code(code_id: int, db: Session = Depends(get_db)):
    existing_code = db.query(Code).filter(Code.id == code_id).first()
    if existing_code is None:
        raise HTTPException(status_code=404, detail="Code not found")

    setattr(existing_code, "status", "inactive")

    db.commit()
    db.refresh(existing_code)

    return {"data": existing_code}
