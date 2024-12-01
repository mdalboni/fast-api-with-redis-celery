from . import *


def test_get_event_by_id_success(create_event_batch_data):
    response = client.get(f"/v1/events")
    assert response.status_code == 200
    output = response.json()
    assert len(output['data']['events']) == 10
    assert output['data']['more_pages'] is True
    assert output['data']['total_items'] == 15
    events = [e['event_id'] for e in output['data']['events']]
    hits, miss = 0, 0
    for event in create_event_batch_data:
        if event.id in events:
            hits += 1
        else:
            miss += 1
    assert hits == 10
    assert miss == 5


def test_get_event_by_id_not_data():
    response = client.get("/v1/events")
    assert response.status_code == 200
    output = response.json()
    assert len(output['data']['events']) == 0
    assert output['data']['more_pages'] is False
    assert output['data']['total_items'] == 0


def test_get_event_by_id_paginated_success(create_event_batch_data):
    response = client.get(f"/v1/events", params={"page": 1})
    assert response.status_code == 200
    output = response.json()
    assert len(output['data']['events']) == 5
    assert output['data']['total_items'] == 15
    assert output['data']['more_pages'] is False
    events = [e['event_id'] for e in output['data']['events']]
    hits, miss = 0, 0
    for event in create_event_batch_data:
        if event.id in events:
            hits += 1
        else:
            miss += 1
    assert hits == 5
    assert miss == 10
