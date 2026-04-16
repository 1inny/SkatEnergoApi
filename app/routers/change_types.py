from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ChangeType
from app.schemas.change_type import ChangeTypeCreate, ChangeTypeUpdate, ChangeTypeOut

router = APIRouter(prefix="/api/changetypes", tags=["ChangeTypes"])


@router.get("", response_model=List[ChangeTypeOut])
def get_change_types(db: Session = Depends(get_db)):
    return db.query(ChangeType).all()


@router.get("/{id}", response_model=ChangeTypeOut)
def get_change_type(id: int, db: Session = Depends(get_db)):
    obj = db.query(ChangeType).filter(ChangeType.id_change_type == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Тип изменения не найден")
    return obj


@router.post("", response_model=ChangeTypeOut, status_code=201)
def create_change_type(dto: ChangeTypeCreate, db: Session = Depends(get_db)):
    obj = ChangeType(change_type_name=dto.change_type_name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{id}", response_model=ChangeTypeOut)
def update_change_type(id: int, dto: ChangeTypeUpdate, db: Session = Depends(get_db)):
    obj = db.query(ChangeType).filter(ChangeType.id_change_type == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Тип изменения не найден")
    obj.change_type_name = dto.change_type_name
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
def delete_change_type(id: int, db: Session = Depends(get_db)):
    obj = db.query(ChangeType).filter(ChangeType.id_change_type == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Тип изменения не найден")
    db.delete(obj)
    db.commit()
