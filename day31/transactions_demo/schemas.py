from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    balance: float

    class Config:
        from_attributes = True