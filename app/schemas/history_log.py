from datetime import datetime
from typing import Optional
from app.schemas.base import BaseSchema


class HistoryLogCreate(BaseSchema):
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    created_at: Optional[datetime] = None
    id_request: Optional[int] = None
    id_appointment: Optional[int] = None
    id_employee: int
    id_change_type: int


class HistoryLogUpdate(BaseSchema):
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    id_employee: int
    id_change_type: int


class HistoryLogOut(BaseSchema):
    id_history: int
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    created_at: Optional[datetime] = None
    id_request: Optional[int] = None
    id_appointment: Optional[int] = None
    id_employee: int
    id_change_type: int
