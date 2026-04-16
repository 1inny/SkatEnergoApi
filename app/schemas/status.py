from pydantic import BaseModel


class StatusBase(BaseModel):
    status_name: str


class StatusCreate(StatusBase):
    pass


class StatusUpdate(StatusBase):
    pass


class StatusOut(StatusBase):
    id_status: int

    model_config = {"from_attributes": True}
