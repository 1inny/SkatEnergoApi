from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class HistoryLogCreate(BaseModel):
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    created_at: Optional[datetime] = None
    id_request: Optional[int] = None
    id_appointment: Optional[int] = None
    id_employee: int
    id_change_type: int


class HistoryLogUpdate(BaseModel):
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    id_employee: int
    id_change_type: int


class HistoryLogOut(BaseModel):
    id_history: int
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    created_at: datetime
    id_request: Optional[int] = None
    id_appointment: Optional[int] = None
    id_employee: int
    id_change_type: int

    model_config = {"from_attributes": True}
