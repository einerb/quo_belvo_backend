from pydantic import BaseModel
from typing import Any, Optional

class SuccessResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    statusCode: int
    error: str
    data: Optional[Any] = None
