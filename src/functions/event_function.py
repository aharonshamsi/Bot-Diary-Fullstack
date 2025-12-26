
from src.services.event_service import fetch_user_events, create_event, resolve_time_extended, execute_deletion, execute_update_event

#========== Get events ========================================
def get_events_function(user_id: int, date: str | None = None):
    return fetch_user_events(user_id, date)



get_events_definition = {
    "name": "get_events",
    "description": (
        "Retrieve all events for the current user. "
        "If a date is provided, return only events that occur on that date."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": (
                    "Optional date filter in YYYY-MM-DD format. "
                    "If omitted, all events are returned."
                )
            }
        }
    }
}






#========== Add event ========================================
def add_event_function(user_id: int, title: str, time_reference: str, description: str | None = None):
    # resolve_time_extended מחזירה datetime כולל שעה אם קיימת
    start_time_dt = resolve_time_extended(time_reference)
    
    data = {
        "title": title,
        "start_time": start_time_dt.isoformat(),
        "description": description
    }
    
    return create_event(user_id, data)






# Definition for OpenAI function calling
add_event_definition = {
    "name": "add_event",
    "description": "Add a new event for the current user",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Title of the event"
            },
            "description": {
                "type": "string",
                "description": "Optional description of the event"
            },
            "time_reference": {
                "type": "string",
                "description": (
                    "Relative date and/or time description, e.g.: "
                    "'tomorrow at 14:00', 'in 3 days at 16:30', "
                    "'next week', 'in one month', etc. "
                    "Model should resolve it into a start_time datetime."
                )
            }
        },
        "required": ["title", "time_reference"]
    }
}




# ========= DELETE EVENT =========
def delete_event_function(user_id: int, event_id: int):
    execute_deletion(user_id, event_id)
    return {
        "status": "success",
        "event_id": event_id
    }



delete_event_definition = {
    "name": "delete_event",
    "description": "Delete one of the user's existing events",
    "parameters": {
        "type": "object",
        "properties": {
            "event_hint": {
                "type": "string",
                "description": "Description or name of the event the user wants to delete"
            }
        },
        "required": ["event_hint"]
    }
}





# ========= UPDATE EVENT =========
def update_event_function(user_id: int, event_id: int, data: dict):
    execute_update_event(user_id, event_id, data)
    return {
        "status": "success",
        "event_id": event_id
    }


update_event_definition = {
    "name": "update_event",
    "description": "Update an existing event for the current user",
    "parameters": {
        "type": "object",
        "properties": {
            "event_hint": {
                "type": "string",
                "description": "Which event the user wants to update (name, description, or date)"
            },
            "data": {
                "type": "object",
                "description": "Only the fields the user wants to change",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "start_time": {"type": "string"},
                    "end_time": {"type": "string"}
                }
            }
        },
        "required": ["event_hint", "data"]
    }
}





