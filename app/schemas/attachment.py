from datetime import datetime
from typing import Optional
from app.schemas.base import BaseSchema


class AttachmentOut(BaseSchema):
    id_attachment: int
    id_appointment: int
    file_name: str
    file_path: str
    file_size: Optional[int] = None
    content_type: Optional[str] = None
    uploaded_at: datetime
    uploaded_by: Optional[int] = None
    uploaded_by_name: Optional[str] = None
    file_url: Optional[str] = None
