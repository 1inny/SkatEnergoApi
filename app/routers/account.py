import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Employee
from app.schemas.auth import ChangePasswordRequest, ChangeLoginRequest

router = APIRouter(prefix="/api/account", tags=["Account"])


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt(12)).decode()


@router.post("/change-password")
def change_password(request: ChangePasswordRequest, db: Session = Depends(get_db)):
    user = db.query(Employee).filter(Employee.id_employee == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    user.password = hash_password(request.new_password)
    db.commit()
    return {"message": "Пароль изменён"}


@router.post("/change-login")
def change_login(request: ChangeLoginRequest, db: Session = Depends(get_db)):
    user = db.query(Employee).filter(Employee.id_employee == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    exists = db.query(Employee).filter(
        Employee.login == request.new_login,
        Employee.id_employee != request.user_id,
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Логин уже занят")
    user.login = request.new_login
    db.commit()
    return {"message": "Логин изменён"}
