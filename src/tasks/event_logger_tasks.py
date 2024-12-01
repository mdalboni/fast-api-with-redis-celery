import logging

from src.databases.redis_event_logger_model import EventLoggerRedis
from src.taskworker import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def process_event_for_user(event_id: str, user_id: str, description: str) -> bool:
    """
    Background task to process an event for a user.
    :param event_id: str
    :param user_id: str
    :param description: str
    :return:
    """
    from src.services.event_logger_service import EventLoggerService
    logger.info('Event %s has been sent to %s: %s.', event_id, user_id, description)
    event_obj = EventLoggerRedis(
        id=event_id,
        user_id=user_id,
        description=description,
        status='processed',
    )
    EventLoggerService().update(event_obj)
    logger.info('Event %s has been processed.', event_id)
    return True
