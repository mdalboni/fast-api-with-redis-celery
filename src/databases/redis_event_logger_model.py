from dataclasses import dataclass
from typing import Optional

from src.utils.redis_objects import RedisObject


@dataclass
class EventLoggerRedis(RedisObject):
    id: str
    user_id: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    redis_key = 'event:'

    @property
    def key(self):
        return self.redis_key + self.id
