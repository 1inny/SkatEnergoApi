from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Address
from app.schemas.address import AddressCreate, AddressUpdate, AddressOut

router = APIRouter(prefix="/api/addresses", tags=["Addresses"])


def _to_out(a: Address) -> AddressOut:
    return AddressOut(
        id_address=a.id_address,
        street=a.street,
        house=a.house,
        apartment=a.apartment,
        id_locality=a.id_locality,
        locality_name=a.locality.locality_name if a.locality else None,
    )


@router.get("", response_model=List[AddressOut])
def get_addresses(db: Session = Depends(get_db)):
    addresses = db.query(Address).options(joinedload(Address.locality)).all()
    return [_to_out(a) for a in addresses]


@router.get("/{id}", response_model=AddressOut)
def get_address(id: int, db: Session = Depends(get_db)):
    a = db.query(Address).options(joinedload(Address.locality)).filter(Address.id_address == id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Адрес не найден")
    return _to_out(a)


@router.post("", response_model=AddressOut, status_code=201)
def create_address(dto: AddressCreate, db: Session = Depends(get_db)):
    obj = Address(**dto.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return _to_out(obj)


@router.put("/{id}", response_model=AddressOut)
def update_address(id: int, dto: AddressUpdate, db: Session = Depends(get_db)):
    obj = db.query(Address).options(joinedload(Address.locality)).filter(Address.id_address == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Адрес не найден")
    for k, v in dto.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return _to_out(obj)


@router.delete("/{id}", status_code=204)
def delete_address(id: int, db: Session = Depends(get_db)):
    obj = db.query(Address).filter(Address.id_address == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Адрес не найден")
    db.delete(obj)
    db.commit()
