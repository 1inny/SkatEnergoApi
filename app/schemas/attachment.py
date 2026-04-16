from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AttachmentOut(BaseModel):
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

    model_config = {"from_attributes": True}
