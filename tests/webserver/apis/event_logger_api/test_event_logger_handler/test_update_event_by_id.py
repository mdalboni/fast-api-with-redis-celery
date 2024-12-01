from . import *


def test_update_event_by_id_success(create_event_data):
    response = client.patch(f"/v1/events/{create_event_data.id}", json={"status": "processed"})
    assert response.status_code == 200
    output = response.json()
    assert output['data']['user_id'] == '123'
    assert output['data']['description'] == 'event description'
    assert output['data']['status'] == 'processed'


def test_update_event_by_id_failure_not_found():
    response = client.patch(f"/v1/events/1234sda", json={"status": "processed"})
    assert response.status_code == 404
    output = response.json()
    assert output.get('data') is None
    assert output['error'] == {'error_code': 10001, 'message': 'Event not found'}


def test_update_event_by_id_failure_bad_input():
    response = client.patch(f"/v1/events/1234sda", json={"status": "completed"})
    assert response.status_code == 422
    output = response.json()
    assert output == [
        {
            'ctx': {'expected': "'pending', 'processed', 'failed' or 'updated'"},
            'input': 'completed',
            'loc': ['body', 'status'],
            'msg': "Input should be 'pending', 'processed', 'failed' or 'updated'",
            'type': 'literal_error',
        }
    ]
