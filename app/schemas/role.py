from app.schemas.base import BaseSchema


class RoleBase(BaseSchema):
    role_name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleOut(RoleBase):
    id_role: int
