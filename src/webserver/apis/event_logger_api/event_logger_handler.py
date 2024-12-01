from fastapi import APIRouter

from src.databases.redis_event_logger_model import EventLoggerRedis
from src.exceptions import ObjectNotFoundError, RedisObjectNotFound
from src.services.event_logger_service import EventLoggerService
from src.webserver.apis.api_schemas import GenericSingleResponse
from src.webserver.apis.events_api.events_schemas import (
    EventListOutput, EventOutput, PatchEventByIdInput,
    PostEventInput, PostEventOutput
)

router = APIRouter(prefix='/v1/events')


@router.get(
    "/",
    response_model=GenericSingleResponse[EventListOutput],
    status_code=200,
    response_model_exclude_none=True
)
async def get_all_events(page: int = 0, limit: int = 10):
    event, more_pages, total_items = EventLoggerService().get_all(page, limit)
    return EventListOutput(
        events=[EventOutput(event_id=e.id, **e.serialize()) for e in event],
        more_pages=more_pages,
        total_items=total_items
    )


@router.post(
    "/",
    response_model=GenericSingleResponse[PostEventOutput],
    status_code=201,
    response_model_exclude_none=True
)
async def create_event(event_input: PostEventInput):
    return PostEventOutput(
        event_id=EventLoggerService().create_and_process(
            event_input.user_id, description=event_input.description
        )
    )


@router.get(
    "/{event_id}",
    response_model=GenericSingleResponse[EventOutput],
    status_code=200,
    response_model_exclude_none=True
)
async def get_event_by_id(event_id: str):
    try:
        event = EventLoggerService().get_by_id(event_id)
    except RedisObjectNotFound:
        raise ObjectNotFoundError('Event not found', status_code=404)
    return EventOutput(
        event_id=event.id,
        user_id=event.user_id,
        status=event.status,
        description=event.description,
    )


@router.patch(
    "/{event_id}",
    response_model=GenericSingleResponse[EventOutput],
    response_model_exclude_none=True
)
async def patch_event_by_id(event_id: str, event: PatchEventByIdInput):
    event = EventLoggerService().update(
        EventLoggerRedis(id=event_id,status=event.status)
    )
    return EventOutput(
        event_id=event.id,
        user_id=event.user_id,
        status=event.status,
        description=event.description,
    )
