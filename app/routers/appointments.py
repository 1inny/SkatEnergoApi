from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Appointment, Request, Employee
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentOut

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])


@router.get("", response_model=List[AppointmentOut])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()


@router.get("/{id}", response_model=AppointmentOut)
def get_appointment(id: int, db: Session = Depends(get_db)):
    obj = db.query(Appointment).filter(Appointment.id_appointment == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Замер не найден")
    return obj


@router.post("", response_model=AppointmentOut)
def create_appointment(dto: AppointmentCreate, db: Session = Depends(get_db)):
    if not db.query(Request).filter(Request.id_request == dto.id_request).first():
        raise HTTPException(status_code=400, detail=f"Заявка с Id={dto.id_request} не найдена")
    if not db.query(Employee).filter(Employee.id_employee == dto.id_employee).first():
        raise HTTPException(status_code=400, detail=f"Сотрудник с Id={dto.id_employee} не найден")
    existing = db.query(Appointment).filter(Appointment.id_request == dto.id_request).first()
    if existing:
        raise HTTPException(status_code=400, detail="Для этой заявки уже назначен замер. Используйте PUT для редактирования.")
    obj = Appointment(
        id_request=dto.id_request,
        id_employee=dto.id_employee,
        start_date_time=dto.start_date_time,
        end_date_time=dto.end_date_time,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{id}", status_code=204)
def update_appointment(id: int, dto: AppointmentUpdate, db: Session = Depends(get_db)):
    obj = db.query(Appointment).filter(Appointment.id_appointment == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Замер не найден")
    if not db.query(Employee).filter(Employee.id_employee == dto.id_employee).first():
        raise HTTPException(status_code=400, detail=f"Сотрудник с Id={dto.id_employee} не найден")
    obj.id_employee = dto.id_employee
    obj.start_date_time = dto.start_date_time
    obj.end_date_time = dto.end_date_time
    db.commit()


@router.delete("/{id}", status_code=204)
def delete_appointment(id: int, db: Session = Depends(get_db)):
    obj = db.query(Appointment).filter(Appointment.id_appointment == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Замер не найден")
    db.delete(obj)
    db.commit()
