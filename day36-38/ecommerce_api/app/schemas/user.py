from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        email: Unique email address of the user.
        name: Full name of the user.
        password: Plain-text password (will be hashed before storage).
        role: User role ('customer' or 'admin'). Defaults to 'customer'."""

    email: EmailStr = Field(..., examples=["john@example.com"])
    name: str = Field(..., min_length=1, examples=["John Doe"])
    password: str = Field(..., min_length=6, examples=["securepass123"])
    role: str = Field(default="customer", examples=["customer", "admin"])


class UserUpdate(BaseModel):
    """
    Schema for updating user information.

    All fields are optional; only provided fields will be updated.

    Attributes:
        name: Full name of the user (optional).
        role: User role (optional).

    """

    name: str | None = Field(None, min_length=1, examples=["Jane Doe"])
    role: str | None = Field(None, examples=["customer", "admin"])


class UserResponse(BaseModel):
    """
    Schema for returning user data in responses.

    Attributes:
        id: Unique user identifier.
        email: Email address.
        name: Full name.
        role: User role ('customer' or 'admin').
        created_at: Timestamp of user creation.
    """

    id: int
    email: EmailStr
    name: str
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)