import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Employee
from app.schemas.auth import LoginRequest
from app.schemas.employee import EmployeeOut

router = APIRouter(prefix="/api/auth", tags=["Auth"])


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def _build_out(user: Employee) -> EmployeeOut:
    return EmployeeOut(
        id_employee=user.id_employee,
        login=user.login,
        first_name=user.first_name,
        last_name=user.last_name,
        id_role=user.id_role,
        role_name=user.role.role_name if user.role else None,
        phone=user.phone,
    )


@router.post("/login", response_model=EmployeeOut)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Employee).filter(Employee.login == request.login).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверный логин или пароль")
    if user.id_role == 3:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Недостаточно прав для входа")
    return _build_out(user)


@router.post("/mobile-login", response_model=EmployeeOut)
def mobile_login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Employee).filter(Employee.login == request.login).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверный логин или пароль")
    if user.id_role != 3:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Доступ только для замерщиков")
    return _build_out(user)
