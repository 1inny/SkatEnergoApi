from datetime import datetime
from typing import Optional
from app.schemas.base import BaseSchema


class RequestCreate(BaseSchema):
    id_client: int
    id_address: int
    id_employee: int
    id_status: int
    created_at: datetime
    appointment_date: Optional[datetime] = None


class RequestUpdate(BaseSchema):
    id_client: int
    id_address: int
    id_employee: int
    id_status: int
    appointment_date: Optional[datetime] = None


class RequestOut(BaseSchema):
    id_request: int
    id_client: int
    client_name: Optional[str] = None
    id_employee: int
    employee_name: Optional[str] = None
    id_address: int
    full_address: Optional[str] = None
    created_at: datetime
    id_status: int
    status_name: Optional[str] = None
    appointment_date: Optional[datetime] = None
