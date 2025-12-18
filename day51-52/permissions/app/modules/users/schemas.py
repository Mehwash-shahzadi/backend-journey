from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    role: str = "user"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str  
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RefreshTokenOut(BaseModel):
    id: int
    token: str
    user_id: int
    is_revoked: bool
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True

# permission schemas

class PermissionCreate(BaseModel):
    name: str
    description: str | None = None

class PermissionOut(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True

class RolePermissionCreate(BaseModel):
    role: str
    permission_id: int

class RolePermissionOut(BaseModel):
    id: int
    role: str
    permission_id: int
    created_at: datetime

    class Config:
        from_attributes = True