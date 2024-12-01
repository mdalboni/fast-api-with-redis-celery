from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

M = TypeVar("M", bound=BaseModel)


class ErrorResponse(BaseModel):
    message: str
    error_code: int
    extras: Optional[dict] = None


class BaseGenericResponse(BaseModel):
    ...


class GenericSingleResponse(BaseGenericResponse, Generic[M]):
    data: Optional[M] = None
    error: Optional[ErrorResponse] = None


class GenericMultipleResponse(BaseGenericResponse, Generic[M]):
    data: Optional[list[M]] = None
    error: Optional[ErrorResponse] = None
