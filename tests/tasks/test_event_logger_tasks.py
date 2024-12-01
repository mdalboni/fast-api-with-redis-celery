from src.tasks import process_event_for_user
from . import *


def test_process_event_for_user(create_event_data):
    assert process_event_for_user(create_event_data.id, '123', 'event description')
    assert EventLoggerService().get_by_id(create_event_data.id).status == 'processed'
