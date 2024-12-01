from typing import Type

from redis import StrictRedis

from src.exceptions import RedisObjectNotFound
from src.utils.redis_objects import RedisObject


class CustomRedis(StrictRedis):
    """
    This is a custom Redis client that extends the original StrictRedis class.
    This class was extended to add some helper functions to save and get objects from Redis.
    """

    def save_redis_object(self, redis_object: RedisObject) -> int:
        """
        Save an object to Redis.
        :param key: Key
        :param redis_object: Value
        :return: int
        """
        return self.hset(redis_object.key, mapping=redis_object.serialize())

    def get_redis_object(self, key: str, redis_object: Type[RedisObject], append_key=True) -> RedisObject:
        """
        Get an object from Redis.
        :param append_key: Append key to redis_object.redis_key for searching
        :param redis_object: Class reference to be generated
        :param key: Key to be used to get the object
        :return: RedisObject
        """
        output = self.hgetall(redis_object.redis_key + key if append_key else key)
        if not output:
            raise RedisObjectNotFound(f'Object {redis_object.redis_key + key} not found')
        return redis_object(**output)  # noqa


def get_redis_client(db=0) -> CustomRedis:
    """
    This is a helper function to get a Redis client.
    We could pass a configuration object to this function, but for now we are using the default configuration.
    Or we could load the configuration from a file or from an environment variables.
    :return: Redis client
    """
    return CustomRedis(host='redis', port=6379, db=db, decode_responses=True)
