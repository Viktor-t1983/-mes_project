from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    success: bool = True
    message: str = ""
    data: Optional[T] = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int
