from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Status, Request
from app.schemas.status import StatusCreate, StatusUpdate, StatusOut

router = APIRouter(prefix="/api/statuses", tags=["Statuses"])


@router.get("", response_model=List[StatusOut])
def get_statuses(db: Session = Depends(get_db)):
    return db.query(Status).all()


@router.get("/{id}", response_model=StatusOut)
def get_status(id: int, db: Session = Depends(get_db)):
    obj = db.query(Status).filter(Status.id_status == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Статус не найден")
    return obj


@router.post("", response_model=StatusOut, status_code=201)
def create_status(dto: StatusCreate, db: Session = Depends(get_db)):
    if db.query(Status).filter(Status.status_name == dto.status_name).first():
        raise HTTPException(status_code=400, detail="Статус с таким названием уже существует")
    obj = Status(status_name=dto.status_name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{id}", response_model=StatusOut)
def update_status(id: int, dto: StatusUpdate, db: Session = Depends(get_db)):
    obj = db.query(Status).filter(Status.id_status == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Статус не найден")
    obj.status_name = dto.status_name
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
def delete_status(id: int, db: Session = Depends(get_db)):
    obj = db.query(Status).filter(Status.id_status == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Статус не найден")
    if db.query(Request).filter(Request.id_status == id).first():
        raise HTTPException(status_code=400, detail="Нельзя удалить статус: есть заявки с этим статусом")
    db.delete(obj)
    db.commit()
