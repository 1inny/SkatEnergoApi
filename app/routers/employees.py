from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from passlib.context import CryptContext

from app.database import get_db
from app.models import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeOut

router = APIRouter(prefix="/api/employees", tags=["Employees"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _to_out(e: Employee) -> EmployeeOut:
    return EmployeeOut(
        id_employee=e.id_employee,
        login=e.login,
        first_name=e.first_name,
        last_name=e.last_name,
        id_role=e.id_role,
        role_name=e.role.role_name if e.role else None,
        phone=e.phone,
    )


@router.get("", response_model=List[EmployeeOut])
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).options(joinedload(Employee.role)).all()
    return [_to_out(e) for e in employees]


@router.get("/{id}", response_model=EmployeeOut)
def get_employee(id: int, db: Session = Depends(get_db)):
    e = db.query(Employee).options(joinedload(Employee.role)).filter(Employee.id_employee == id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return _to_out(e)


@router.post("", status_code=201)
def create_employee(dto: EmployeeCreate, db: Session = Depends(get_db)):
    employee = Employee(
        login=dto.login,
        password=pwd_context.hash(dto.password),
        first_name=dto.first_name,
        last_name=dto.last_name,
        id_role=dto.id_role,
        phone=dto.phone,
    )
    db.add(employee)
    db.commit()
    return {}


@router.put("/{id}", status_code=204)
def update_employee(id: int, dto: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id_employee == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    employee.login = dto.login
    employee.first_name = dto.first_name
    employee.last_name = dto.last_name
    employee.id_role = dto.id_role
    employee.phone = dto.phone
    if dto.new_password:
        employee.password = pwd_context.hash(dto.new_password)
    db.commit()


@router.delete("/{id}", status_code=204)
def delete_employee(id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id_employee == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    db.delete(employee)
    db.commit()
