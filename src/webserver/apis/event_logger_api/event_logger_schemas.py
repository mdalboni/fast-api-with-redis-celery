from typing import Literal

from pydantic import BaseModel, Field, field_validator

EventLoggerStatuses = Literal['pending', 'processed', 'failed', 'updated']


class PostEventLoggerInput(BaseModel):
    user_id: str = Field(min_length=1)
    description: str = Field(min_length=5)

    @field_validator('user_id')
    def user_id_must_not_be_empty(cls, v):
        if len(v) == 0:
            raise ValueError('user_id must not be empty')
        return v

    @field_validator('description')
    def description_must_be_longer_than_5(cls, v):
        if len(v) < 5:
            raise ValueError('description must be longer than 5 characters')
        return v


class PostEventLoggerResponse(BaseModel):
    event_id: str


class PatchEventLoggerByIdInput(BaseModel):
    status: EventLoggerStatuses


class EventLoggerResponse(BaseModel):
    model_config = {
        'extra': 'ignore'
    }

    event_id: str
    user_id: str
    description: str
    status: EventLoggerStatuses


class EventLoggerListResponse(BaseModel):
    events: list[EventLoggerResponse]
    more_pages: bool
    total_items: int
