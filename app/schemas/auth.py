from app.schemas.base import BaseSchema


class LoginRequest(BaseSchema):
    login: str
    password: str


class ChangePasswordRequest(BaseSchema):
    user_id: int
    new_password: str


class ChangeLoginRequest(BaseSchema):
    user_id: int
    new_login: str
