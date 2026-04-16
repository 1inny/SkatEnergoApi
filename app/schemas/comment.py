from datetime import datetime
from typing import Optional
from app.schemas.base import BaseSchema


class CommentCreate(BaseSchema):
    comment_text: str
    created_at: datetime
    id_request: Optional[int] = None
    id_appointment: Optional[int] = None
    id_employee: int


class CommentUpdate(BaseSchema):
    comment_text: str


class CommentOut(BaseSchema):
    id_comment: int
    id_request: Optional[int] = None
    id_appointment: Optional[int] = None
    id_employee: int
    employee_name: Optional[str] = None
    comment_text: str
    created_at: datetime
