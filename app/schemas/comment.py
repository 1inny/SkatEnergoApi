from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CommentCreate(BaseModel):
    comment_text: str
    created_at: datetime
    id_request: Optional[int] = None
    id_appointment: Optional[int] = None
    id_employee: int


class CommentUpdate(BaseModel):
    comment_text: str


class CommentOut(BaseModel):
    id_comment: int
    comment_text: str
    created_at: datetime
    id_request: Optional[int] = None
    id_appointment: Optional[int] = None
    id_employee: int

    model_config = {"from_attributes": True}
