from pydantic import BaseModel


class LoginRequest(BaseModel):
    login: str
    password: str


class ChangePasswordRequest(BaseModel):
    user_id: int
    new_password: str


class ChangeLoginRequest(BaseModel):
    user_id: int
    new_login: str
