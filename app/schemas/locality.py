from app.schemas.base import BaseSchema


class LocalityBase(BaseSchema):
    locality_name: str


class LocalityCreate(LocalityBase):
    pass


class LocalityUpdate(LocalityBase):
    pass


class LocalityOut(LocalityBase):
    id_locality: int
