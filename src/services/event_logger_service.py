from uuid_extensions import uuid7str

from src.databases.redis_db import get_redis_client
from src.databases.redis_event_logger_model import EventLoggerRedis
from src.tasks import process_event_for_user


class EventLoggerService:

    def __init__(self, redis_client=None):
        """
        Initialize the service with a redis client or get a default one.
        We can use this redis client to use an existing client or to mock it in tests.
        :param redis_client:
        """
        self.redis_client = redis_client if redis_client else get_redis_client()

    def create(self, user_id: str, description: str) -> EventLoggerRedis:
        """
        Create an event and returns the id
        :param user_id: User id
        :param description: Description
        :return: Event id
        """

        event = EventLoggerRedis(
            user_id=user_id,
            description=description,
            status='pending',
            id=uuid7str(),
        )
        if not self.redis_client.save_redis_object(event):
            raise Exception('Could not save event') # TODO add a custom exception
        return event

    def create_and_process(self, user_id: str, description: str) -> str:
        """
        Create an event and returns the id, and process it on the background
        :param user_id: User id
        :param description: Description
        :return: Event id
        """

        event = self.create(user_id, description)
        process_event_for_user.apply_async((event.id, user_id, description))
        return event.id

    def update(self, event: EventLoggerRedis) -> EventLoggerRedis:
        """
        Updates an existing event and returns if the operation was successful
        :param event: EventRedis object
        :return: int of number of fields updated
        """

        redis_event = self.get_by_id(event.id)
        redis_event.status = event.status
        self.redis_client.save_redis_object(redis_event)
        return redis_event

    def get_by_id(self, event_id: str) -> EventLoggerRedis:
        """
        Get the status of an event by the id
        :param event_id: Event id
        :return: EventRedis object
        """
        return self.redis_client.get_redis_object(event_id, EventLoggerRedis)  # noqa

    def get_all(self, page=0, limit=10) -> tuple[list[EventLoggerRedis], bool, int]:
        """
        Get all events paginated
        :return: List of events and a boolean indicating if there are more pages
        """
        keys = self.redis_client.keys('event:*')
        starts_at = page * limit
        more_pages = len(keys[starts_at:]) >= limit
        total_items = len(keys)
        keys = keys[starts_at:starts_at + limit]
        events = [
            self.redis_client.get_redis_object(key, EventLoggerRedis, append_key=False)
            for key in keys
        ]
        return events, more_pages, total_items  # noqa
