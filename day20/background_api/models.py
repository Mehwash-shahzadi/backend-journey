from pydantic import BaseModel, EmailStr, Field

# Input model
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int = Field(gt=0)

# Output model
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
