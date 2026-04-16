from typing import Optional
from pydantic import BaseModel


class ClientBase(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    phone: str
    email: Optional[str] = None
    id_subject_type: int


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    pass


class ClientOut(ClientBase):
    id_client: int

    model_config = {"from_attributes": True}
