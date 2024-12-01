from urllib.request import Request

from fastapi import FastAPI

from code.webserver.apis import events_router
from code.webserver.apis.api_schemas import GenericMultipleResponse, GenericSingleResponse

app = FastAPI()
app.include_router(events_router)


@app.middleware("http")
async def context_middleware(request: Request, call_next):
    response = await call_next(request)
    print(response)
    return (
        GenericSingleResponse(data=response)
        if isinstance(response, list)
        else GenericMultipleResponse(data=response)
    )


# @app.exception_handler(Exception)
# async def validation_exception_handler(request, exc):
#     response = Generic(
#         jsonable_encoder(
#             {
#                 "errors": [Error(kind=type(exc).__name__, detail=str(exc))] + request.state.errors,
#                 "context": request.state.context,
#                 "data": None,
#             }
#         ),
#         status_code=500,
#     )
#     return response
