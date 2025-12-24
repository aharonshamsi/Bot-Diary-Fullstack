
from src.services.event_service import fetch_user_events

#========== Get events ========================================
def get_events_function(user_id: int, date: str | None = None):
    return fetch_user_events(user_id, date)



get_events_definition = {
    "name": "get_events",
    "description": "Get events for the current user, optionally filtered by date",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "Date in YYYY-MM-DD format (optional)"
            }
        }
    }
}






#========== Get events ========================================

