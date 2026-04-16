from datetime import datetime
from typing import Optional
from app.schemas.base import BaseSchema


class AppointmentCreate(BaseSchema):
    id_request: int
    id_employee: int
    start_date_time: datetime
    end_date_time: Optional[datetime] = None


class AppointmentUpdate(BaseSchema):
    id_employee: int
    start_date_time: datetime
    end_date_time: Optional[datetime] = None


class AppointmentOut(BaseSchema):
    id_appointment: int
    id_request: int
    id_employee: int
    start_date_time: datetime
    end_date_time: Optional[datetime] = None
