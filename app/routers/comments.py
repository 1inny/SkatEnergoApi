from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Comment
from app.schemas.comment import CommentCreate, CommentUpdate, CommentOut

router = APIRouter(prefix="/api/comments", tags=["Comments"])


@router.get("", response_model=List[CommentOut])
def get_comments(db: Session = Depends(get_db)):
    return db.query(Comment).all()


@router.get("/{id}", response_model=CommentOut)
def get_comment(id: int, db: Session = Depends(get_db)):
    obj = db.query(Comment).filter(Comment.id_comment == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return obj


@router.post("", response_model=CommentOut, status_code=201)
def create_comment(dto: CommentCreate, db: Session = Depends(get_db)):
    obj = Comment(**dto.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{id}", response_model=CommentOut)
def update_comment(id: int, dto: CommentUpdate, db: Session = Depends(get_db)):
    obj = db.query(Comment).filter(Comment.id_comment == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    obj.comment_text = dto.comment_text
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
def delete_comment(id: int, db: Session = Depends(get_db)):
    obj = db.query(Comment).filter(Comment.id_comment == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    db.delete(obj)
    db.commit()
