from pydantic import BaseModel

class ErrorResponse(BaseModel):
    """
    Standard error response model used in OpenAPI responses.
    """
    detail: str
