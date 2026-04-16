from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Comment
from app.schemas.comment import CommentCreate, CommentUpdate, CommentOut

router = APIRouter(prefix="/api/comments", tags=["Comments"])


def _to_out(c: Comment) -> CommentOut:
    return CommentOut(
        id_comment=c.id_comment,
        id_request=c.id_request,
        id_appointment=c.id_appointment,
        id_employee=c.id_employee,
        employee_name=f"{c.employee.last_name} {c.employee.first_name}" if c.employee else None,
        comment_text=c.comment_text,
        created_at=c.created_at,
    )


def _query(db: Session):
    return db.query(Comment).options(joinedload(Comment.employee))


@router.get("", response_model=List[CommentOut])
def get_comments(db: Session = Depends(get_db)):
    return [_to_out(c) for c in _query(db).all()]


@router.get("/{id}", response_model=CommentOut)
def get_comment(id: int, db: Session = Depends(get_db)):
    c = _query(db).filter(Comment.id_comment == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return _to_out(c)


@router.post("", response_model=CommentOut, status_code=201)
def create_comment(dto: CommentCreate, db: Session = Depends(get_db)):
    obj = Comment(
        comment_text=dto.comment_text,
        created_at=dto.created_at,
        id_request=dto.id_request,
        id_appointment=dto.id_appointment,
        id_employee=dto.id_employee,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    c = _query(db).filter(Comment.id_comment == obj.id_comment).first()
    return _to_out(c)


@router.put("/{id}", response_model=CommentOut)
def update_comment(id: int, dto: CommentUpdate, db: Session = Depends(get_db)):
    obj = _query(db).filter(Comment.id_comment == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    obj.comment_text = dto.comment_text
    db.commit()
    db.refresh(obj)
    return _to_out(obj)


@router.delete("/{id}", status_code=204)
def delete_comment(id: int, db: Session = Depends(get_db)):
    obj = db.query(Comment).filter(Comment.id_comment == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    db.delete(obj)
    db.commit()
