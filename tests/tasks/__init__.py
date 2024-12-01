import pytest
from fastapi.testclient import TestClient

from src.databases.redis_db import get_redis_client
from src.services.event_logger_service import EventLoggerService
from src.webserver.main import app

client = TestClient(app, raise_server_exceptions=False)
redis_client = get_redis_client()


@pytest.fixture(autouse=True)
def teardown_function():
    redis_client.flushdb()
    yield
    redis_client.flushdb()


@pytest.fixture
def create_event_data(user_id='123', description='event description'):
    return EventLoggerService().create(user_id, description)


@pytest.fixture
def create_event_batch_data(user_id='123', description='event description'):
    return [
        EventLoggerService().create(user_id, description)
        for _ in range(15)
    ]
