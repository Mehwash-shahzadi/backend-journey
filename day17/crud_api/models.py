from pydantic import BaseModel, EmailStr, Field

# Model for creating a new user
class UserCreate(BaseModel):
    name: str
    email: EmailStr                 
    age: int = Field(gt=0)  
          
#Model for returning user data (output)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int