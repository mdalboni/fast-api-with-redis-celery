from datetime import datetime, timedelta, timezone

from uuid_extensions import uuid_to_datetime

from . import *


def test_create_event_success(mock_apply_async):
    event_data = {
        "user_id": "123",
        "description": "Event description",
    }

    start = datetime.now(timezone.utc)
    response = client.post("/v1/events/", json=event_data)
    assert response.status_code == 201
    output = response.json()
    assert output['data']['event_id']
    delta = uuid_to_datetime(output['data']['event_id']) - start
    assert timedelta(seconds=1) > delta, f'Event id should be recent it is over 1s: {delta}.'


def test_create_event_failure_bad_input_missing_key():
    event_data = {
        "description": "Event description",
    }
    response = client.post("/v1/events/", json=event_data)
    assert response.status_code == 400
    assert response.json() == [
        {'input': {'description': 'Event description'}, 'loc': ['body', 'user_id'], 'msg': 'Field required',
         'type': 'missing'}
    ]


def test_create_event_failure_bad_input_validator():
    event_data = [
        (
            {"user_id": None, "description": "Event description"},
            [{'input': None, 'loc': ['body', 'user_id'], 'msg': 'Input should be a valid string',
              'type': 'string_type'}]
        ),
        (
            {"user_id": "123", "description": "Even"},
            [{'ctx': {'min_length': 5}, 'input': 'Even', 'loc': ['body', 'description'],
              'msg': 'String should have at least 5 characters', 'type': 'string_too_short'}]
        ),
    ]
    for item in event_data:
        response = client.post("/v1/events/", json=item[0])
        assert response.status_code == 400
        assert response.json() == item[1]


def test_create_event_failure_internal_server_error(mock_apply_async_exception):
    event_data = {
        "user_id": "123",
        "description": "Event description",
    }
    response = client.post("/v1/events/", json=event_data)
    assert response.status_code == 500
    assert response.json() == {
        'error': {
            'error_code': 10000,
            'message': 'Too bad, something went wrong.\nThe problem is with us not you.'
        }
    }
