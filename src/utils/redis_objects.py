from dataclasses import asdict


class RedisObject:
    """
    Base class for all redis objects
    """
    redis_key: str

    @property
    def key(self):
        raise NotImplementedError

    def serialize(self) -> dict:
        return asdict(self)  # noqa
