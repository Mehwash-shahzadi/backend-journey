from pydantic import BaseModel


class Register(BaseModel):
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool
