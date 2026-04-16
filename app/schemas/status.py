from app.schemas.base import BaseSchema


class StatusBase(BaseSchema):
    status_name: str


class StatusCreate(StatusBase):
    pass


class StatusUpdate(StatusBase):
    pass


class StatusOut(StatusBase):
    id_status: int
