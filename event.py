from models import increment_event, get_event_status
import events

"""
Can be triggered from:
    - walking somewhere
    - talking to somebody (beginning of dialog)
    - talking to somebody (end of dialog)
    - a npc walking somewhere
"""


def execute_event(event: str, al: 'All'):
    status = get_event_status(event)
    function_name = f"_{event}_{status}"
    increment_event(event)

    try:
        method = getattr(events, function_name)
        method(al)
    except AttributeError:
        print(f'Could not find method {function_name} in events.py!')
