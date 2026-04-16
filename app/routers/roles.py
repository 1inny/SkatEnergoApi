from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Role, Employee
from app.schemas.role import RoleCreate, RoleUpdate, RoleOut

router = APIRouter(prefix="/api/roles", tags=["Roles"])


@router.get("", response_model=List[RoleOut])
def get_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()


@router.get("/{id}", response_model=RoleOut)
def get_role(id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id_role == id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    return role


@router.post("", response_model=RoleOut, status_code=201)
def create_role(dto: RoleCreate, db: Session = Depends(get_db)):
    if db.query(Role).filter(Role.role_name == dto.role_name).first():
        raise HTTPException(status_code=400, detail="Роль с таким названием уже существует")
    role = Role(role_name=dto.role_name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.put("/{id}", response_model=RoleOut)
def update_role(id: int, dto: RoleUpdate, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id_role == id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    role.role_name = dto.role_name
    db.commit()
    db.refresh(role)
    return role


@router.delete("/{id}", status_code=204)
def delete_role(id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id_role == id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    if db.query(Employee).filter(Employee.id_role == id).first():
        raise HTTPException(status_code=400, detail="Нельзя удалить роль: есть сотрудники с этой ролью")
    db.delete(role)
    db.commit()
