

from src.functions.event_function import get_events_function, get_events_definition
from src.functions.event_function import add_event_function, add_event_definition
from src.functions.event_function import delete_event_function, delete_event_definition
from src.functions.event_function import update_event_function, update_event_definition


FUNCTION_DEFINITIONS = [
    get_events_definition,
    add_event_definition,
    delete_event_definition,
    update_event_definition
]

FUNCTION_MAP = {
    "get_events": get_events_function,
    "add_event": add_event_function,
    "delete_event": delete_event_function,
    "update_event": update_event_function
}
