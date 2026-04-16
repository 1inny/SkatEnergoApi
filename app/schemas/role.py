from pydantic import BaseModel


class RoleBase(BaseModel):
    role_name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleOut(RoleBase):
    id_role: int

    model_config = {"from_attributes": True}
