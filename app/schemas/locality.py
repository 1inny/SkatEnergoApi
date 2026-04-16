from pydantic import BaseModel


class LocalityBase(BaseModel):
    locality_name: str


class LocalityCreate(LocalityBase):
    pass


class LocalityUpdate(LocalityBase):
    pass


class LocalityOut(LocalityBase):
    id_locality: int

    model_config = {"from_attributes": True}
