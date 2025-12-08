from pydantic import BaseModel, Field, ConfigDict


class CategoryCreate(BaseModel):

    name: str = Field(..., min_length=1, examples=["Electronics"])
    description: str | None = Field(None, examples=["Electronic devices and gadgets"])


class CategoryUpdate(BaseModel):

    name: str | None = Field(None, min_length=1, examples=["Gadgets"])
    description: str | None = Field(None, examples=["Updated description"])


class CategoryResponse(BaseModel):
   
    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)