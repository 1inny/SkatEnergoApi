from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SubjectType
from app.schemas.subject_type import SubjectTypeCreate, SubjectTypeUpdate, SubjectTypeOut

router = APIRouter(prefix="/api/subjecttypes", tags=["SubjectTypes"])


@router.get("", response_model=List[SubjectTypeOut])
def get_subject_types(db: Session = Depends(get_db)):
    return db.query(SubjectType).all()


@router.get("/{id}", response_model=SubjectTypeOut)
def get_subject_type(id: int, db: Session = Depends(get_db)):
    obj = db.query(SubjectType).filter(SubjectType.id_subject_type == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Тип субъекта не найден")
    return obj


@router.post("", response_model=SubjectTypeOut, status_code=201)
def create_subject_type(dto: SubjectTypeCreate, db: Session = Depends(get_db)):
    obj = SubjectType(subject_type_name=dto.subject_type_name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{id}", response_model=SubjectTypeOut)
def update_subject_type(id: int, dto: SubjectTypeUpdate, db: Session = Depends(get_db)):
    obj = db.query(SubjectType).filter(SubjectType.id_subject_type == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Тип субъекта не найден")
    obj.subject_type_name = dto.subject_type_name
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
def delete_subject_type(id: int, db: Session = Depends(get_db)):
    obj = db.query(SubjectType).filter(SubjectType.id_subject_type == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Тип субъекта не найден")
    db.delete(obj)
    db.commit()
