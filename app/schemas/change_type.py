from pydantic import BaseModel


class ChangeTypeBase(BaseModel):
    change_type_name: str


class ChangeTypeCreate(ChangeTypeBase):
    pass


class ChangeTypeUpdate(ChangeTypeBase):
    pass


class ChangeTypeOut(ChangeTypeBase):
    id_change_type: int

    model_config = {"from_attributes": True}
