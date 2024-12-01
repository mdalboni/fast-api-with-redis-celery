from src.databases.redis_event_model import EventLoggerRedis
from src.taskworker import celery_app


@celery_app.task
def process_event_for_user(event_id: str, user_id: str, description: str):
    from src.services.event_service import EventLoggerService
    print(f'Event {event_id} has been sent to {user_id}: {description}.')
    event_obj = EventLoggerRedis(
        id=event_id,
        user_id=user_id,
        description=description,
        status='processed',
    )
    EventLoggerService().update_event(event_obj)
    print(f'Event {event_id} has been processed.')
    return True
