import os
import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Attachment, Appointment
from app.schemas.attachment import AttachmentOut

router = APIRouter(prefix="/api/attachments", tags=["Attachments"])

UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def _to_out(a: Attachment, base_url: str = "") -> AttachmentOut:
    return AttachmentOut(
        id_attachment=a.id_attachment,
        id_appointment=a.id_appointment,
        file_name=a.file_name,
        file_path=a.file_path,
        file_size=a.file_size,
        content_type=a.content_type,
        uploaded_at=a.uploaded_at,
        uploaded_by=a.uploaded_by,
        uploaded_by_name=f"{a.employee.last_name} {a.employee.first_name}" if a.employee else "",
        file_url=f"{base_url}{a.file_path}" if base_url else a.file_path,
    )


# GET /api/attachments/byappointment/{id}  (было ByAppointment)
@router.get("/byappointment/{appointment_id}", response_model=List[AttachmentOut])
def get_attachments_by_appointment(
    appointment_id: int, request: Request, db: Session = Depends(get_db)
):
    attachments = (
        db.query(Attachment)
        .options(joinedload(Attachment.employee))
        .filter(Attachment.id_appointment == appointment_id)
        .order_by(Attachment.uploaded_at.desc())
        .all()
    )
    base_url = str(request.base_url).rstrip("/")
    return [_to_out(a, base_url) for a in attachments]


# POST /api/attachments/upload  (было Upload)
@router.post("/upload", response_model=AttachmentOut)
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    # C# клиент шлёт поля camelCase
    appointment_id: int = Form(..., alias="appointmentId"),
    uploaded_by: int = Form(1, alias="uploadedBy"),
    db: Session = Depends(get_db),
):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Файл не выбран")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Размер файла превышает 10 МБ")

    if not db.query(Appointment).filter(Appointment.id_appointment == appointment_id).first():
        raise HTTPException(status_code=400, detail="Замер не найден")

    os.makedirs(UPLOADS_DIR, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4()}{ext}"
    file_path_on_disk = os.path.join(UPLOADS_DIR, unique_name)

    with open(file_path_on_disk, "wb") as f:
        f.write(contents)

    relative_path = f"/uploads/{unique_name}"
    content_type = file.content_type or "application/octet-stream"

    attachment = Attachment(
        id_appointment=appointment_id,
        file_name=file.filename,
        file_path=relative_path,
        file_size=len(contents),
        content_type=content_type,
        uploaded_at=datetime.now(),
        uploaded_by=uploaded_by,
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    base_url = str(request.base_url).rstrip("/")
    return AttachmentOut(
        id_attachment=attachment.id_attachment,
        id_appointment=attachment.id_appointment,
        file_name=attachment.file_name,
        file_path=attachment.file_path,
        file_size=attachment.file_size,
        content_type=attachment.content_type,
        uploaded_at=attachment.uploaded_at,
        uploaded_by=attachment.uploaded_by,
        file_url=f"{base_url}{relative_path}",
    )


# GET /api/attachments/download/{id}  (было Download)
@router.get("/download/{id}")
def download_file(id: int, db: Session = Depends(get_db)):
    attachment = db.query(Attachment).filter(Attachment.id_attachment == id).first()
    if not attachment:
        raise HTTPException(status_code=404, detail=f"Вложение с ID {id} не найдено")

    file_path_on_disk = os.path.join(
        UPLOADS_DIR, os.path.basename(attachment.file_path)
    )
    if not os.path.exists(file_path_on_disk):
        raise HTTPException(status_code=404, detail=f"Файл не найден на сервере: {attachment.file_name}")

    content_type = attachment.content_type or "application/octet-stream"
    return FileResponse(
        path=file_path_on_disk,
        media_type=content_type,
        filename=attachment.file_name,
    )


# DELETE /api/attachments/{id}
@router.delete("/{id}", status_code=204)
def delete_attachment(id: int, db: Session = Depends(get_db)):
    attachment = db.query(Attachment).filter(Attachment.id_attachment == id).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="Вложение не найдено")

    file_path_on_disk = os.path.join(
        UPLOADS_DIR, os.path.basename(attachment.file_path)
    )
    if os.path.exists(file_path_on_disk):
        os.remove(file_path_on_disk)

    db.delete(attachment)
    db.commit()
