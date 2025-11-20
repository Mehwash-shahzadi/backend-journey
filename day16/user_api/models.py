from pydantic import BaseModel, EmailStr, Field

# Model for creating a new user
class UserCreate(BaseModel):
    email: EmailStr                 
    password: str = Field(min_length=8)
    age: int = Field(gt=0)  
          
#model for user response
class UserResponse(BaseModel):
    email: EmailStr
    age: int
