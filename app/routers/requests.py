from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Request, Status, HistoryLog
from app.schemas.request import RequestCreate, RequestUpdate, RequestOut

router = APIRouter(prefix="/api/requests", tags=["Requests"])


def _to_out(r: Request) -> RequestOut:
    address = r.address
    locality_name = address.locality.locality_name if address and address.locality else ""
    full_address = ""
    if address:
        full_address = f"{locality_name}, {address.street}, д.{address.house}"
        if address.apartment:
            full_address += f", кв.{address.apartment}"
    return RequestOut(
        id_request=r.id_request,
        id_client=r.id_client,
        client_name=f"{r.client.last_name} {r.client.first_name}" if r.client else None,
        id_employee=r.id_employee,
        employee_name=f"{r.employee.last_name} {r.employee.first_name}" if r.employee else None,
        id_address=r.id_address,
        full_address=full_address,
        created_at=r.created_at,
        id_status=r.id_status,
        status_name=r.status.status_name if r.status else None,
        appointment_date=r.appointment_date,
    )


def _load_request(db: Session, id: int) -> Request:
    return (
        db.query(Request)
        .options(
            joinedload(Request.client),
            joinedload(Request.employee),
            joinedload(Request.address).joinedload(Request.address.property.mapper.class_.locality),
            joinedload(Request.status),
        )
        .filter(Request.id_request == id)
        .first()
    )


@router.get("", response_model=List[RequestOut])
def get_requests(db: Session = Depends(get_db)):
    rows = (
        db.query(Request)
        .options(
            joinedload(Request.client),
            joinedload(Request.employee),
            joinedload(Request.address).joinedload(Request.address.property.mapper.class_.locality),
            joinedload(Request.status),
        )
        .all()
    )
    return [_to_out(r) for r in rows]


@router.get("/{id}", response_model=RequestOut)
def get_request(id: int, db: Session = Depends(get_db)):
    r = _load_request(db, id)
    if not r:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return _to_out(r)


@router.post("", response_model=RequestOut, status_code=201)
def create_request(dto: RequestCreate, db: Session = Depends(get_db)):
    obj = Request(
        id_client=dto.id_client,
        id_address=dto.id_address,
        id_employee=dto.id_employee,
        id_status=dto.id_status,
        created_at=dto.created_at,
        appointment_date=dto.appointment_date,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    r = _load_request(db, obj.id_request)
    return _to_out(r)


@router.put("/{id}", status_code=204)
def update_request(id: int, dto: RequestUpdate, db: Session = Depends(get_db)):
    obj = db.query(Request).filter(Request.id_request == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    status_changed = obj.id_status != dto.id_status
    old_status_id = obj.id_status

    obj.id_client = dto.id_client
    obj.id_address = dto.id_address
    obj.id_employee = dto.id_employee
    obj.id_status = dto.id_status
    obj.appointment_date = dto.appointment_date

    if status_changed:
        old_status = db.query(Status).filter(Status.id_status == old_status_id).first()
        new_status = db.query(Status).filter(Status.id_status == dto.id_status).first()
        log = HistoryLog(
            id_request=id,
            id_employee=dto.id_employee,
            id_change_type=2,
            field_name="Статус",
            old_value=old_status.status_name if old_status else str(old_status_id),
            new_value=new_status.status_name if new_status else str(dto.id_status),
            created_at=datetime.now(),
        )
        db.add(log)

    db.commit()


@router.delete("/{id}", status_code=204)
def delete_request(id: int, db: Session = Depends(get_db)):
    obj = db.query(Request).filter(Request.id_request == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    db.delete(obj)
    db.commit()
