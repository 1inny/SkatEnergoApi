from app.schemas.base import BaseSchema


class ChangeTypeBase(BaseSchema):
    change_type_name: str


class ChangeTypeCreate(ChangeTypeBase):
    pass


class ChangeTypeUpdate(ChangeTypeBase):
    pass


class ChangeTypeOut(ChangeTypeBase):
    id_change_type: int
