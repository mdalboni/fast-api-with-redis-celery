from . import *


def test_get_event_by_id_success(create_event_data):
    response = client.get(f"/v1/events/{create_event_data}")
    assert response.status_code == 200
    output = response.json()
    assert output['data']['user_id'] == '123'
    assert output['data']['description'] == 'event description'
    assert output['data']['status'] == 'pending'

def test_get_event_by_id_failure_not_found():
    response = client.get("/v1/events/123")
    assert response.status_code == 404
    assert response.json() == {'error': {'error_code': 10001, 'message': 'Event not found'}}
