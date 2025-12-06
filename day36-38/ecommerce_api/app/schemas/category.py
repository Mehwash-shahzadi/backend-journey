"""
Category schemas for product categorization.

Schemas:
    - CategoryCreate: Input schema for creating a new category (POST).
    - CategoryUpdate: Input schema for updating category information (PUT).
    - CategoryResponse: Output schema for returning category data (GET).
"""

from pydantic import BaseModel, Field, ConfigDict


class CategoryCreate(BaseModel):
    """
    Schema for creating a new category.

    Attributes:
        name: Unique category name.
        description: Optional description of the category.

    Example:
        >>> cat = CategoryCreate(
        ...     name="Electronics",
        ...     description="Electronic devices and gadgets"
        ... )
    """

    name: str = Field(..., min_length=1, examples=["Electronics"])
    description: str | None = Field(None, examples=["Electronic devices and gadgets"])


class CategoryUpdate(BaseModel):
    """
    Schema for updating category information.

    All fields are optional; only provided fields will be updated.

    Attributes:
        name: Category name (optional).
        description: Category description (optional).

    Example:
        >>> update = CategoryUpdate(name="Gadgets")
    """

    name: str | None = Field(None, min_length=1, examples=["Gadgets"])
    description: str | None = Field(None, examples=["Updated description"])


class CategoryResponse(BaseModel):
    """
    Schema for returning category data in responses.

    Attributes:
        id: Unique category identifier.
        name: Category name.
        description: Category description (if available).

    Example:
        >>> cat = CategoryResponse(
        ...     id=1,
        ...     name="Electronics",
        ...     description="Electronic devices"
        ... )
    """

    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)