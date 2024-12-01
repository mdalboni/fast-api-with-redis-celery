from urllib.request import Request

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from src.exceptions import ApplicationError
from src.webserver.apis import events_router
from src.webserver.apis.api_schemas import ErrorResponse, GenericErrorResponse

app = FastAPI()
app.include_router(events_router)


@app.middleware("http")
async def context_middleware(request: Request, call_next):
    """
    We can use this middleware to add some perform actions before and after the processing.
    :param request: Request object
    :param call_next: Callable
    """
    return await call_next(request)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    This function is used to handle the validation errors that are raised by the FastAPI framework.
    We can add more behaviors if it is QA env or production. To show more or less data.
    :param request: Request object
    :param exc: Exception
    :return: JSONResponse
    """
    return JSONResponse(exc.errors(), status_code=422)


@app.exception_handler(Exception)
async def internal_server_error_handler(request, exc):
    """
    This function is used to handle the exceptions that are not caught by the application.
    We can add more behaviors if it is QA env or production. To show more or less data
    :param request: Request object
    :param exc: Exception
    :return: JSONResponse
    """
    error_response = GenericErrorResponse(
        error=ErrorResponse(
            message=f"Too bad, something went wrong.\nThe problem is with us not you.",
            error_code=10000,
        )
    )
    return JSONResponse(
        content=error_response.model_dump(exclude_none=True),
        status_code=500
    )


@app.exception_handler(ApplicationError)
async def raised_http_exception(request, exc: ApplicationError):
    """
    This function is used to handle the exceptions we raise in the application.
    We can add more behaviors if it is QA env or production. To show more or less data.
    :param request: Request object
    :param exc: Exception
    :return: JSONResponse
    """
    error_response = GenericErrorResponse(
        error=ErrorResponse(
            message=exc.message,
            error_code=exc.error_code,
            extras=exc.extras
        )
    )
    return JSONResponse(
        content=error_response.model_dump(exclude_none=True),
        status_code=exc.status_code
    )
