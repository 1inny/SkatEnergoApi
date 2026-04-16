from typing import Optional
from app.schemas.base import BaseSchema


class AddressBase(BaseSchema):
    street: str
    house: str
    apartment: Optional[str] = None
    id_locality: int


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class AddressOut(AddressBase):
    id_address: int
    locality_name: Optional[str] = None
