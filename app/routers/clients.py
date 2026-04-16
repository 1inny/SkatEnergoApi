from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Client
from app.schemas.client import ClientCreate, ClientUpdate, ClientOut

router = APIRouter(prefix="/api/clients", tags=["Clients"])


@router.get("", response_model=List[ClientOut])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()


@router.get("/{id}", response_model=ClientOut)
def get_client(id: int, db: Session = Depends(get_db)):
    obj = db.query(Client).filter(Client.id_client == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return obj


@router.post("", response_model=ClientOut, status_code=201)
def create_client(dto: ClientCreate, db: Session = Depends(get_db)):
    obj = Client(**dto.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{id}", response_model=ClientOut)
def update_client(id: int, dto: ClientUpdate, db: Session = Depends(get_db)):
    obj = db.query(Client).filter(Client.id_client == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    for k, v in dto.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
def delete_client(id: int, db: Session = Depends(get_db)):
    obj = db.query(Client).filter(Client.id_client == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    db.delete(obj)
    db.commit()
