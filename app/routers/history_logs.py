from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import HistoryLog
from app.schemas.history_log import HistoryLogCreate, HistoryLogUpdate, HistoryLogOut

router = APIRouter(prefix="/api/historylogs", tags=["HistoryLogs"])


def _to_out(h: HistoryLog) -> HistoryLogOut:
    return HistoryLogOut(
        id_history=h.id_history,
        id_request=h.id_request,
        id_appointment=h.id_appointment,
        id_employee=h.id_employee,
        employee_name=f"{h.employee.last_name} {h.employee.first_name}" if h.employee else None,
        id_change_type=h.id_change_type,
        change_type_name=h.change_type.change_type_name if h.change_type else None,
        field_name=h.field_name,
        old_value=h.old_value,
        new_value=h.new_value,
        created_at=h.created_at,
    )


def _query(db: Session):
    return (
        db.query(HistoryLog)
        .options(
            joinedload(HistoryLog.employee),
            joinedload(HistoryLog.change_type),
        )
    )


@router.get("", response_model=List[HistoryLogOut])
def get_history_logs(db: Session = Depends(get_db)):
    return [_to_out(h) for h in _query(db).all()]


@router.get("/{id}", response_model=HistoryLogOut)
def get_history_log(id: int, db: Session = Depends(get_db)):
    h = _query(db).filter(HistoryLog.id_history == id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Запись истории не найдена")
    return _to_out(h)


@router.post("", response_model=HistoryLogOut, status_code=201)
def create_history_log(dto: HistoryLogCreate, db: Session = Depends(get_db)):
    obj = HistoryLog(
        id_request=dto.id_request,
        id_appointment=dto.id_appointment,
        id_employee=dto.id_employee,
        id_change_type=dto.id_change_type,
        field_name=dto.field_name,
        old_value=dto.old_value,
        new_value=dto.new_value,
        created_at=dto.created_at or datetime.now(),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    h = _query(db).filter(HistoryLog.id_history == obj.id_history).first()
    return _to_out(h)


@router.put("/{id}", response_model=HistoryLogOut)
def update_history_log(id: int, dto: HistoryLogUpdate, db: Session = Depends(get_db)):
    obj = _query(db).filter(HistoryLog.id_history == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Запись истории не найдена")
    obj.field_name = dto.field_name
    obj.old_value = dto.old_value
    obj.new_value = dto.new_value
    obj.id_employee = dto.id_employee
    obj.id_change_type = dto.id_change_type
    db.commit()
    db.refresh(obj)
    h = _query(db).filter(HistoryLog.id_history == obj.id_history).first()
    return _to_out(h)


@router.delete("/{id}", status_code=204)
def delete_history_log(id: int, db: Session = Depends(get_db)):
    obj = db.query(HistoryLog).filter(HistoryLog.id_history == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Запись истории не найдена")
    db.delete(obj)
    db.commit()
