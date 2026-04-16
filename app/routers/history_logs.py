from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import HistoryLog
from app.schemas.history_log import HistoryLogCreate, HistoryLogUpdate, HistoryLogOut

router = APIRouter(prefix="/api/historylogs", tags=["HistoryLogs"])


@router.get("", response_model=List[HistoryLogOut])
def get_history_logs(db: Session = Depends(get_db)):
    return db.query(HistoryLog).all()


@router.get("/{id}", response_model=HistoryLogOut)
def get_history_log(id: int, db: Session = Depends(get_db)):
    obj = db.query(HistoryLog).filter(HistoryLog.id_history == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Запись истории не найдена")
    return obj


@router.post("", response_model=HistoryLogOut, status_code=201)
def create_history_log(dto: HistoryLogCreate, db: Session = Depends(get_db)):
    data = dto.model_dump()
    if not data.get("created_at"):
        data["created_at"] = datetime.now()
    obj = HistoryLog(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{id}", response_model=HistoryLogOut)
def update_history_log(id: int, dto: HistoryLogUpdate, db: Session = Depends(get_db)):
    obj = db.query(HistoryLog).filter(HistoryLog.id_history == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Запись истории не найдена")
    for k, v in dto.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
def delete_history_log(id: int, db: Session = Depends(get_db)):
    obj = db.query(HistoryLog).filter(HistoryLog.id_history == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Запись истории не найдена")
    db.delete(obj)
    db.commit()
