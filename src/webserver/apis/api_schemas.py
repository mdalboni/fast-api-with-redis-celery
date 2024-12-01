from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, model_validator

M = TypeVar("M", bound=BaseModel)


class ErrorResponse(BaseModel):
    message: str
    error_code: int
    extras: Optional[dict] = None


class BaseGenericResponse(BaseModel):
    ...


class GenericErrorResponse(BaseModel):
    error: ErrorResponse


class GenericSingleResponse(BaseGenericResponse, Generic[M]):
    data: M = None

    @model_validator(mode='before')  # noqa
    @classmethod
    def handle_data(cls, data):
        return {'data': data}


class GenericMultipleResponse(BaseGenericResponse, Generic[M]):
    data: list[M] = None

    @model_validator(mode='before')  # noqa
    @classmethod
    def handle_data(cls, data):
        return {'data': data}
