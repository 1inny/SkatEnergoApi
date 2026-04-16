from typing import Optional
from app.schemas.base import BaseSchema


class EmployeeCreate(BaseSchema):
    login: str
    password: str
    first_name: str
    last_name: str
    id_role: int
    phone: Optional[str] = None


class EmployeeUpdate(BaseSchema):
    login: str
    first_name: str
    last_name: str
    id_role: int
    phone: Optional[str] = None
    new_password: Optional[str] = None


class EmployeeOut(BaseSchema):
    id_employee: int
    login: str
    first_name: str
    last_name: str
    id_role: int
    role_name: Optional[str] = None
    phone: Optional[str] = None
