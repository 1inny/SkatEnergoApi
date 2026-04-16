from typing import Optional
from pydantic import BaseModel


class ClientBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: Optional[str] = None
    id_subject_type: Optional[int] = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    pass


class ClientOut(ClientBase):
    id_client: int

    model_config = {"from_attributes": True}
