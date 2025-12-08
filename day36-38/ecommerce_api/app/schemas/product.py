from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from .category import CategoryResponse


class ProductCreate(BaseModel):
    """
    Schema for creating a new product.

    Attributes:
        name: Product name.
        price: Product price (decimal with 2 decimals).
        stock: Initial stock quantity (defaults to 0).
        category_ids: List of category IDs to associate with the product.
    """

    name: str = Field(..., min_length=1, examples=["Laptop"])
    price: Decimal = Field(..., gt=0, decimal_places=2, examples=[Decimal("999.99")])
    stock: int = Field(default=0, ge=0, examples=[10])
    category_ids: list[int] = Field(default_factory=list, examples=[[1, 2, 3]])


class ProductUpdate(BaseModel):
    """
    Schema for updating product information.

    All fields are optional; only provided fields will be updated.

    Attributes:
        name: Product name (optional).
        price: Product price (optional).
        stock: Stock quantity (optional).
        category_ids: List of category IDs (optional).


    """

    name: str | None = Field(None, min_length=1, examples=["Laptop Pro"])
    price: Decimal | None = Field(None, gt=0, decimal_places=2, examples=[Decimal("899.99")])
    stock: int | None = Field(None, ge=0, examples=[5])
    category_ids: list[int] | None = Field(None, examples=[[1, 3]])


class ProductResponse(BaseModel):
    """
    Schema for returning product data with nested categories.

    Attributes:
        id: Unique product identifier.
        name: Product name.
        price: Product price.
        stock: Current stock quantity.
        created_at: Timestamp of product creation.
        categories: List of associated categories.
    """

    id: int
    name: str
    price: Decimal
    stock: int
    created_at: datetime
    categories: list[CategoryResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)