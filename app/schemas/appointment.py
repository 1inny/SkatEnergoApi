from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    id_request: int
    id_employee: int
    start_date_time: datetime
    end_date_time: Optional[datetime] = None


class AppointmentUpdate(BaseModel):
    id_employee: int
    start_date_time: datetime
    end_date_time: Optional[datetime] = None


class AppointmentOut(BaseModel):
    id_appointment: int
    id_request: int
    id_employee: int
    start_date_time: datetime
    end_date_time: Optional[datetime] = None

    model_config = {"from_attributes": True}
