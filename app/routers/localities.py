from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Locality
from app.schemas.locality import LocalityCreate, LocalityUpdate, LocalityOut

router = APIRouter(prefix="/api/localities", tags=["Localities"])


@router.get("", response_model=List[LocalityOut])
def get_localities(db: Session = Depends(get_db)):
    return db.query(Locality).all()


@router.get("/{id}", response_model=LocalityOut)
def get_locality(id: int, db: Session = Depends(get_db)):
    obj = db.query(Locality).filter(Locality.id_locality == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Населённый пункт не найден")
    return obj


@router.post("", response_model=LocalityOut, status_code=201)
def create_locality(dto: LocalityCreate, db: Session = Depends(get_db)):
    obj = Locality(locality_name=dto.locality_name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{id}", response_model=LocalityOut)
def update_locality(id: int, dto: LocalityUpdate, db: Session = Depends(get_db)):
    obj = db.query(Locality).filter(Locality.id_locality == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Населённый пункт не найден")
    obj.locality_name = dto.locality_name
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
def delete_locality(id: int, db: Session = Depends(get_db)):
    obj = db.query(Locality).filter(Locality.id_locality == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Населённый пункт не найден")
    db.delete(obj)
    db.commit()
