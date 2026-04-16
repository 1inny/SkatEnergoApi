from typing import Optional
from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str
    id_role: int
    phone: Optional[str] = None


class EmployeeUpdate(BaseModel):
    login: str
    first_name: str
    last_name: str
    id_role: int
    phone: Optional[str] = None
    new_password: Optional[str] = None


class EmployeeOut(BaseModel):
    id_employee: int
    login: str
    first_name: str
    last_name: str
    id_role: int
    role_name: Optional[str] = None
    phone: Optional[str] = None

    model_config = {"from_attributes": True}
